"""Camada de compatibilidade com a ITMO_FS 0.3.3 (quirks reais da API).

Encapsula descobertas empíricas para que o restante do itmofs-lab tenha uma
API uniforme e limpa. NÃO altera o pacote ITMO_FS.
"""

from __future__ import annotations

import importlib.metadata as _md

import numpy as np

import ITMO_FS as _I


def itmo_version() -> str:
    try:
        return _md.version("ITMO_FS")
    except Exception:
        return getattr(_I, "__version__", "desconhecida")


# Strings de medida registradas no UnivariateFilter (fonte: GLOB_MEASURE).
try:
    from ITMO_FS.filters.univariate.measures import GLOB_MEASURE as _GLOB_MEASURE
    REGISTERED_MEASURE_STRINGS = set(_GLOB_MEASURE.keys())
except Exception:  # pragma: no cover
    REGISTERED_MEASURE_STRINGS = set()

MEASURE_STRING = {
    "f_ratio_measure": "FRatio", "gini_index": "GiniIndex",
    "su_measure": "SymmetricUncertainty", "fechner_corr": "FechnerCorr",
    "information_gain": "InformationGain", "reliefF_measure": "ReliefF",
    "chi2_measure": "Chi2", "spearman_corr": "SpearmanCorr",
    "pearson_corr": "PearsonCorr", "kendall_corr": "KendallCorr",
    "fit_criterion_measure": "FitCriterion",
}


def measure_for_uf(measure_name: str):
    """Argumento `measure` do UnivariateFilter: string registrada ou callable."""
    ms = MEASURE_STRING.get(measure_name)
    if ms and ms in REGISTERED_MEASURE_STRINGS:
        return ms
    fn = getattr(_I, measure_name, None)
    if fn is None:
        raise KeyError(f"measure desconhecida: {measure_name!r}")
    return fn


# Cutting rules — operam sobre dict {feature: score}.
CR_FACTORY = {
    "select_k_best": _I.select_k_best, "select_k_worst": _I.select_k_worst,
    "select_best_by_value": _I.select_best_by_value,
    "select_worst_by_value": _I.select_worst_by_value,
    "select_best_percentage": _I.select_best_percentage,
    "select_worst_percentage": _I.select_worst_percentage,
}
CR_NAME_FOR_UF = {
    "select_k_best": "K best", "select_k_worst": "K worst",
    "select_best_by_value": "Best by value", "select_worst_by_value": "Worst by value",
    "select_best_percentage": "Best by percentage", "select_worst_percentage": "Worst by percentage",
}


def make_cutting_rule(name: str, param):
    if name not in CR_FACTORY:
        raise KeyError(f"cutting rule desconhecida: {name!r}")
    return CR_FACTORY[name](param)


def get_selected(obj):
    for a in ("selected_features", "selected_features_", "_selected_features"):
        if hasattr(obj, a):
            v = getattr(obj, a)
            if v is not None:
                return [int(i) for i in v]
    return None


def get_scores(obj, n_features=None):
    for a in ("feature_scores", "feature_scores_", "scores_"):
        if hasattr(obj, a):
            val = getattr(obj, a)
            if isinstance(val, dict):
                size = n_features or (max(int(k) for k in val) + 1)
                arr = np.full(size, np.nan, dtype=float)
                for k, v in val.items():
                    arr[int(k)] = float(v)
                return arr
            return np.asarray(val, dtype=float)
    return None


def run_selector(obj, X_train, y_train=None, n_features=None):
    """Adaptador para seletores estilo run()/feature_ranking().

    Retorna (selected_indices, scores_or_None). Trata TraceRatioLaplacian
    (run -> (indices, score, lambda)).
    """
    if type(obj).__name__ == "TraceRatioLaplacian":
        idx, score, _lam = obj.run(X_train, y_train)
        return [int(i) for i in idx], np.asarray(score, dtype=float)
    W = obj.run(X_train, y_train) if y_train is not None else obj.run(X_train)
    if hasattr(obj, "feature_ranking"):
        ranking = np.atleast_1d(obj.feature_ranking(W))
        idx = [int(i) for i in ranking][:(n_features or len(ranking))]
        Wl = np.asarray(W)
        scores = np.linalg.norm(Wl, axis=1) if Wl.ndim == 2 else Wl.astype(float)
        return idx, scores
    Wl = np.asarray(W, dtype=float).reshape(-1)
    order = np.argsort(Wl)[::-1]
    return [int(i) for i in order[:(n_features or len(order))]], Wl


# Bugs conhecidos (para mensagens de erro claras, não mascarar).
KNOWN_BUGS = {
    "fit_criterion_measure": "np.empty(np.unique(y)) -> TypeError; quebrado na 0.3.3.",
    "SPEC_unsupervised": "run(X, y=None) falha; use modo label-aware.",
    "MCFS_dot": "scheme='dot' quebrado (typo ___scheme_dot); use '0-1' ou 'heat'.",
    "BestSum_predict": "predict() passa dict como cutting_rule; use fit()+cut().",
    "RecursiveElimination": "usa list.remove em ndarray -> AttributeError.",
    "FilterWrapperHybrid": "internamente usa RecursiveElimination (mesmo bug).",
    "HillClimbingWrapper": "compara dict com int -> TypeError.",
    "TPhMGWO": "usa np.float (removido no numpy>=1.24) -> AttributeError.",
    "AddDelWrapper": "score chamado como int -> TypeError na 0.3.3.",
    "SimulatedAnnealing": "fit exige test_x/test_y (leakage por design).",
    "qpfs_filter": "requer solver de QP (quadprog) ausente.",
}
