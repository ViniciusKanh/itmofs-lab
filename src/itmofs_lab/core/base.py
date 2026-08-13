"""Classes-base do itmofs-lab: API uniforme sobre a ITMO_FS.

Todas expõem o mesmo contrato:
    m = Metodo(**params)
    m.fit(X, y)                 # ajusta SÓ no treino
    X_sel = m.transform(X)      # aplica as mesmas colunas
    m.selected_                 # índices selecionados
    m.selected_names_           # nomes (se feature_names informado)
    m.scores_                   # vetor de scores (ou None)
    m.info()                    # ajuda: o que entra e o que sai

A regra anti-leakage é responsabilidade do usuário no split; os métodos aqui
nunca usam dados de teste no fit.
"""

from __future__ import annotations

import numpy as np

import ITMO_FS as I

from . import compat
from .spec import MethodSpec


class NotSupportedError(RuntimeError):
    """Método presente na API mas não executável na versão instalada."""


class FSMethod:
    """Base abstrata. Subclasses implementam ``_fit_impl``."""

    SPEC: MethodSpec = None  # definido por subclasse/instância

    def __init__(self, spec: MethodSpec = None, **params):
        self.spec = spec or self.SPEC
        self.params = params
        self.selected_ = None
        self.scores_ = None
        self.ranking_ = None
        self.selected_names_ = None
        self._n_features = None

    # ------------------------------------------------------------------ API
    def fit(self, X, y=None, feature_names=None):
        X = np.asarray(X, dtype=float)
        self._n_features = X.shape[1]
        self._feature_names = list(feature_names) if feature_names is not None \
            else [f"f{i}" for i in range(X.shape[1])]
        self._fit_impl(X, None if y is None else np.asarray(y))
        if self.selected_ is not None:
            self.selected_ = [int(i) for i in self.selected_]
            self.selected_names_ = [self._feature_names[i] for i in self.selected_]
            if self.ranking_ is None:
                self.ranking_ = list(self.selected_)
        return self

    def transform(self, X):
        if self.selected_ is None:
            raise RuntimeError("chame fit() antes de transform()")
        return np.asarray(X, dtype=float)[:, self.selected_]

    def fit_transform(self, X, y=None, feature_names=None):
        return self.fit(X, y, feature_names).transform(X)

    # ----------------------------------------------------------------- ajuda
    def info(self) -> str:
        """Texto de ajuda: o que entra e o que sai deste método."""
        return self.spec.io_text()

    def info_dict(self) -> dict:
        return self.spec.as_dict()

    def describe(self):
        print(self.info())

    def _fit_impl(self, X, y):  # pragma: no cover
        raise NotImplementedError


# --------------------------------------------------------------------------- #
# Filtros univariados (score) via UnivariateFilter
# --------------------------------------------------------------------------- #
class UnivariateScore(FSMethod):
    def __init__(self, spec=None, measure=None, k=10, cutting_rule="select_k_best",
                 cutting_param=None, **params):
        super().__init__(spec, **params)
        self.measure = measure or self.spec.itmo_symbol
        self.cutting_rule = cutting_rule
        self.cutting_param = k if cutting_param is None else cutting_param

    def _fit_impl(self, X, y):
        marg = compat.measure_for_uf(self.measure)
        uf = I.UnivariateFilter(marg, (compat.CR_NAME_FOR_UF[self.cutting_rule], self.cutting_param))
        uf.fit(X, y)
        self.selected_ = compat.get_selected(uf)
        self.scores_ = compat.get_scores(uf, n_features=X.shape[1])
        self._uf = uf


# --------------------------------------------------------------------------- #
# Filtros multivariados (critério) via MultivariateFilter
# --------------------------------------------------------------------------- #
class MultivariateCriterion(FSMethod):
    def __init__(self, spec=None, n_features=10, beta=None, gamma=None, **params):
        super().__init__(spec, **params)
        self.n_features = n_features
        self.beta = beta
        self.gamma = gamma

    def _fit_impl(self, X, y):
        kw = {}
        if self.beta is not None:
            kw["beta"] = self.beta
        if self.gamma is not None:
            kw["gamma"] = self.gamma
        mf = I.MultivariateFilter(self.spec.itmo_symbol, self.n_features, **kw)
        mf.fit(X, y)
        self.selected_ = compat.get_selected(mf)   # ordem de seleção
        self.ranking_ = list(self.selected_)
        self.scores_ = None                          # sem score global


# --------------------------------------------------------------------------- #
# Seletores standalone com fit/transform (DISR, FCBF, STIR, TraceRatioFisher, MOS)
# --------------------------------------------------------------------------- #
class StandaloneSelector(FSMethod):
    def __init__(self, spec=None, factory=None, supervised=True, **params):
        super().__init__(spec, **params)
        self._factory = factory
        self.supervised = supervised

    def _fit_impl(self, X, y):
        obj = self._factory(self.params)
        obj.fit(X, y) if (self.supervised and y is not None) else obj.fit(X)
        sel = compat.get_selected(obj)
        if sel is None:
            Xs = obj.transform(X)
            sel = list(range(Xs.shape[1]))  # fallback
        self.selected_ = sel
        self.scores_ = compat.get_scores(obj, n_features=X.shape[1])
        self._obj = obj


# --------------------------------------------------------------------------- #
# Seletores esparsos/não supervisionados via run()/feature_ranking()
# --------------------------------------------------------------------------- #
class SparseSelector(FSMethod):
    def __init__(self, spec=None, factory=None, n_features=10, mode="unsupervised", **params):
        super().__init__(spec, **params)
        self._factory = factory
        self.n_features = n_features
        self.mode = mode  # unsupervised | label_aware

    def _fit_impl(self, X, y):
        obj = self._factory(self.params)
        use_y = (self.mode == "label_aware")
        sel, scores = compat.run_selector(obj, X, y if use_y else None, n_features=self.n_features)
        self.selected_ = sel[:self.n_features]
        self.ranking_ = list(self.selected_)
        if scores is not None and np.ndim(scores) == 1 and len(scores) == X.shape[1]:
            self.scores_ = scores
        self._obj = obj


# --------------------------------------------------------------------------- #
# Ensembles
# --------------------------------------------------------------------------- #
class WeightBasedEnsemble(FSMethod):
    def __init__(self, spec=None, base_measures=("GiniIndex", "FRatio"),
                 k=10, cutting_rule="select_k_best", cutting_param=None, weights=None, **params):
        super().__init__(spec, **params)
        self.base_measures = list(base_measures)
        self.cutting_rule = cutting_rule
        self.cutting_param = k if cutting_param is None else cutting_param
        self.weights = weights

    def _fit_impl(self, X, y):
        p = X.shape[1]
        bases = [I.UnivariateFilter(m, ("K best", p)) for m in self.base_measures]
        wb = I.WeightBased(bases)
        wb.fit(X, y)
        w = None if self.weights is None else np.asarray(self.weights, dtype=float)
        wref = w if w is not None else np.ones(len(bases)) / len(bases)
        agg = I.weight_fusion(wb.feature_scores, wref)
        self.scores_ = np.array([agg[k] for k in sorted(agg)], dtype=float)
        cr = compat.make_cutting_rule(self.cutting_rule, self.cutting_param)
        wb.transform(X, cr, weights=w)
        self.selected_ = [int(i) for i in wb.selected_features]
        self._obj = wb


class MixedEnsemble(FSMethod):
    def __init__(self, spec=None, base_measures=("spearman_corr", "pearson_corr"),
                 k=10, **params):
        super().__init__(spec, **params)
        self.base_measures = list(base_measures)
        self.k = k

    def _fit_impl(self, X, y):
        fns = [getattr(I, m) for m in self.base_measures]
        mx = I.Mixed(fns)
        mx.fit(X, y)
        mx.transform(X, self.k)
        self.selected_ = [int(i) for i in mx._selected_features]
        self.ranking_ = list(self.selected_)
        self.scores_ = None
        self._obj = mx


class BestSumEnsemble(FSMethod):
    def __init__(self, spec=None, base_measures=("GiniIndex", "FRatio"),
                 k_each=8, k=10, cutting_rule="select_k_best", cutting_param=None, **params):
        super().__init__(spec, **params)
        self.base_measures = list(base_measures)
        self.k_each = k_each
        self.cutting_rule = cutting_rule
        self.cutting_param = k if cutting_param is None else cutting_param

    def _fit_impl(self, X, y):
        from .adapters import UnivariateModelAdapter
        models = [UnivariateModelAdapter(m, k=self.k_each) for m in self.base_measures]
        bs = I.BestSum(models, compat.make_cutting_rule(self.cutting_rule, self.cutting_param))
        bs.fit(X, y)
        self.selected_ = [int(i) for i in bs.cut()]  # predict() é bugado; usamos cut()
        self.scores_ = np.array([bs.features.get(i, 0.0) for i in range(X.shape[1])], dtype=float)
        self._obj = bs


class MelifHybrid(FSMethod):
    def __init__(self, spec=None, base_measures=("GiniIndex", "FRatio"),
                 k=10, estimator=None, scorer=None, **params):
        super().__init__(spec, **params)
        self.base_measures = list(base_measures)
        self.k = k
        self.estimator = estimator
        self.scorer = scorer

    def _fit_impl(self, X, y):
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import f1_score
        p = X.shape[1]
        ens = I.WeightBased([I.UnivariateFilter(m, ("K best", p)) for m in self.base_measures])
        est = self.estimator or LogisticRegression(max_iter=500)
        scorer = self.scorer or (lambda yt, yp: f1_score(yt, yp, average="macro"))
        ml = I.Melif(ens, scorer=scorer)
        ml.fit(X, y, est, compat.make_cutting_rule("select_k_best", self.k))
        Xs = ml.transform(X)
        # Melif seleciona colunas; recuperamos índices via selected_features se houver
        sel = compat.get_selected(ml)
        if sel is None:
            sel = list(range(Xs.shape[1]))
        self.selected_ = sel
        self._obj = ml


# --------------------------------------------------------------------------- #
# Wrappers (estimator + measure/score). Só os que funcionam na 0.3.3.
# --------------------------------------------------------------------------- #
class WrapperSelector(FSMethod):
    def __init__(self, spec=None, estimator=None, n_features=10, measure=None, **params):
        super().__init__(spec, **params)
        self.estimator = estimator
        self.n_features = n_features
        self.measure = measure

    def _fit_impl(self, X, y):
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score
        est = self.estimator or LogisticRegression(max_iter=500)
        # medida como FUNÇÃO simples score(y_true, y_pred) — evita que a ITMO_FS
        # a interprete como 'scoring' do sklearn (que rejeita métrica crua).
        score = self.measure or (lambda y_true, y_pred: accuracy_score(y_true, y_pred))
        cls = getattr(I, self.spec.itmo_symbol)
        # BackwardSelection interpreta n_features como "features a REMOVER"; para
        # manter a API uniforme (n_features = manter), convertemos para p - k.
        if self.spec.itmo_symbol == "BackwardSelection":
            n_arg = max(1, X.shape[1] - self.n_features)
        else:
            n_arg = self.n_features
        obj = cls(est, n_arg, score)
        obj.fit(X, y)
        self.selected_ = compat.get_selected(obj)
        self._obj = obj


# --------------------------------------------------------------------------- #
# Método presente na API porém não executável (bug/dependência/leakage)
# --------------------------------------------------------------------------- #
class BrokenMethod(FSMethod):
    def _fit_impl(self, X, y):
        raise NotSupportedError(
            f"{self.spec.name}: {self.spec.status} — {self.spec.quirks}\n"
            f"Este método está catalogado e documentado, mas não é executável na "
            f"ITMO_FS {compat.itmo_version()}."
        )


# --------------------------------------------------------------------------- #
# Componente de apoio (VDM) — não seleciona features
# --------------------------------------------------------------------------- #
class SupportComponent(FSMethod):
    def _fit_impl(self, X, y):
        raise NotSupportedError(
            f"{self.spec.name} é componente de apoio ({self.spec.summary}); "
            f"não produz subconjunto de features. Use .run(X, y) diretamente na ITMO_FS."
        )
