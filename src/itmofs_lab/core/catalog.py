"""Catálogo único de métodos do itmofs-lab (fonte de verdade dos metadados).

Cada entrada associa: MethodSpec (o que entra/sai) + classe-base + kwargs default
+ (quando necessário) uma factory que constrói o objeto ITMO_FS.

Os resumos vêm da documentação oficial da API ITMO_FS; status/quirks vêm da
auditoria empírica da versão 0.3.3.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Type

import ITMO_FS as I

from . import base as B
from .spec import MethodSpec


@dataclass
class Entry:
    spec: MethodSpec
    cls: Type[B.FSMethod]
    kwargs: dict
    factory: Optional[Callable] = None   # para standalone/sparse


ENTRIES: list[Entry] = []


def _add(cls, kwargs=None, factory=None, **spec_kw):
    ENTRIES.append(Entry(MethodSpec(**spec_kw), cls, kwargs or {}, factory))


# ============================================================ UNIVARIADOS (score)
_UNI = [
    ("f_ratio_measure", "F-ratio (Fisher score)", "Calcula o Fisher score de cada feature (separação entre classes)."),
    ("gini_index", "Gini index", "Índice de Gini: medida de dispersão estatística por feature."),
    ("su_measure", "Symmetric Uncertainty", "Correlação informacional SU(X,Y)=2*I(X;Y)/(H(X)+H(Y))."),
    ("spearman_corr", "Spearman correlation", "Correlação de Spearman de cada feature com o alvo."),
    ("pearson_corr", "Pearson correlation", "Correlação de Pearson de cada feature com o alvo."),
    ("fechner_corr", "Fechner correlation", "Correlação de sinal (Fechner) de cada feature."),
    ("kendall_corr", "Kendall correlation", "Correlação de sinal (Kendall) de cada feature."),
    ("reliefF_measure", "ReliefF", "Medida ReliefF baseada em vizinhos mais próximos."),
    ("chi2_measure", "Chi-squared", "Estatística qui-quadrado entre feature e classe."),
    ("information_gain", "Information gain", "Informação mútua I(X;Y)=H(X)-H(X|Y) por feature."),
    ("anova", "ANOVA F-test", "Estatística F de ANOVA por feature."),
    ("laplacian_score", "Laplacian score", "Score laplaciano (não supervisionado); menor é melhor."),
]
for name, disp, summ in _UNI:
    corr = name.endswith("_corr")
    _add(B.UnivariateScore, kwargs=dict(measure=name, k=10),
         name=name, display=disp, family="filters.univariate",
         component_type="score_function", summary=summ, itmo_symbol=name,
         itmo_signature=f"{name}(X, y)  |  UnivariateFilter('{name}', ('K best', k))",
         status="OK", needs_X=True,
         y="not_used" if name == "laplacian_score" else "required",
         requires_discrete=name in ("information_gain", "su_measure"),
         requires_nonnegative=name == "chi2_measure",
         recommends_scaling=("standard" if name in ("reliefF_measure", "laplacian_score")
                             else ("minmax" if name == "chi2_measure"
                                   else ("discretize" if name in ("information_gain", "su_measure") else "optional"))),
         params={"k": "nº de features a manter (cutting rule 'K best')",
                 "cutting_rule": "select_k_best|select_best_percentage|...",
                 "cutting_param": "parâmetro da cutting rule (k, percent, value)"},
         outputs_scores=True, outputs_ranking=True, outputs_subset=True,
         selected_attr="selected_", transforms_test=True, cutting_rule="obrigatória (via UnivariateFilter)",
         quirks=("correlação com sinal: 'K best' usa score BRUTO — associações fortemente "
                 "negativas podem ser ignoradas; considere magnitude." if corr else ""),
         example=f">>> from itmofs_lab import get\n>>> m = get('{name}', k=10).fit(X_train, y_train)\n>>> X_sel = m.transform(X_test); m.selected_names_",
         references="ITMO_FS.filters.univariate")

# fit_criterion_measure — presente mas quebrado
_add(B.BrokenMethod, name="fit_criterion_measure", display="Fit Criterion", family="filters.univariate",
     component_type="score_function", summary="Critério de ajuste por classe (centros/variâncias).",
     itmo_symbol="fit_criterion_measure", itmo_signature="fit_criterion_measure(X, y)",
     status="BROKEN_IN_0_3_3", outputs_scores=True,
     quirks="bug: np.empty(np.unique(y)) -> TypeError em qualquer entrada.")

# qpfs_filter — dependência ausente
_add(B.BrokenMethod, name="qpfs_filter", display="QPFS", family="filters.univariate",
     component_type="score_function", summary="Quadratic Programming Feature Selection.",
     itmo_symbol="qpfs_filter", itmo_signature="qpfs_filter(X, y, r, sigma, solv, fn)",
     status="DEPENDENCY_MISSING", quirks="requer solver de QP (quadprog) ausente.")

# ============================================================ CRITÉRIOS multivariados
_CRIT = [
    ("MIM", "Mutual Information Maximization", "Maximiza relevância (informação mútua) com o alvo."),
    ("MRMR", "mRMR", "Máxima relevância e mínima redundância."),
    ("JMI", "Joint Mutual Information", "Informação mútua conjunta (complementaridade)."),
    ("CIFE", "CIFE", "Conditional Infomax Feature Extraction."),
    ("MIFS", "MIFS", "Relevância menos penalização de redundância (parâmetro beta)."),
    ("CMIM", "CMIM", "Conditional Mutual Info Maximisation."),
    ("ICAP", "ICAP", "Interaction Capping."),
    ("DCSF", "DCSF", "Dynamic change of selected feature."),
    ("CFR", "CFR", "Maximiza correlação e minimiza redundância."),
    ("MRI", "MRI", "Max-Relevance and Max-Independence."),
    ("IWFS", "IWFS", "Interaction Weight based feature scoring."),
    ("generalizedCriteria", "Generalized Criteria", "Combinação linear de relevância/redundância/dependência (beta, gamma)."),
]
for name, disp, summ in _CRIT:
    kw = dict(n_features=10)
    if name == "MIFS":
        kw["beta"] = 0.5
    if name == "generalizedCriteria":
        kw.update(beta=0.5, gamma=0.5)
    _add(B.MultivariateCriterion, kwargs=kw,
         name=name, display=disp, family="filters.multivariate",
         component_type="criterion_function", summary=summ, itmo_symbol=name,
         itmo_signature=f"MultivariateFilter('{name}', n_features)", status="OK",
         y="required", requires_discrete=True, recommends_scaling="discretize",
         params={"n_features": "nº de features a selecionar (processo sequencial)",
                 **({"beta": "peso de redundância"} if name in ("MIFS", "generalizedCriteria") else {}),
                 **({"gamma": "peso de dependência condicional"} if name == "generalizedCriteria" else {})},
         outputs_scores=False, outputs_ranking=True, outputs_subset=True,
         quirks="sem score global comparável; ranking = ordem de seleção (score_available=false).",
         example=f">>> m = get('{name}', n_features=10).fit(X_train_disc, y_train)\n>>> m.selected_",
         references="ITMO_FS.filters.multivariate")

# ============================================================ STANDALONE multivariados
def _f_disr(p): return I.DISRWithMassive(expected_size=p.get("expected_size", 10))
def _f_fcbf(p): return I.FCBFDiscreteFilter()
def _f_stir(p): return I.STIR(n_features_to_keep=p.get("n_features", 10))
def _f_trf(p): return I.TraceRatioFisher(p.get("n_features", 10))

_add(B.StandaloneSelector, kwargs=dict(expected_size=10), factory=_f_disr,
     name="DISRWithMassive", display="DISR with Massive", family="filters.multivariate",
     component_type="standalone_selector",
     summary="Double Input Symmetric Relevance (kASSI); maximiza info mútua evitando densidade multivariada grande.",
     itmo_symbol="DISRWithMassive", itmo_signature="DISRWithMassive(expected_size).fit(X,y).transform(X)",
     status="OK", requires_discrete=True, recommends_scaling="discretize",
     params={"expected_size": "nº de features esperado"}, outputs_scores=False,
     references="ITMO_FS.filters.multivariate")
_add(B.StandaloneSelector, kwargs={}, factory=_f_fcbf,
     name="FCBFDiscreteFilter", display="FCBF (discrete)", family="filters.multivariate",
     component_type="standalone_selector",
     summary="Fast Correlation Based Filter para dados discretos (info mútua; remove redundância).",
     itmo_symbol="FCBFDiscreteFilter", itmo_signature="FCBFDiscreteFilter().fit(X,y).transform(X)",
     status="OK", requires_discrete=True, recommends_scaling="discretize", outputs_scores=False,
     params={}, quirks="define automaticamente o nº de features (limiar de correlação).",
     references="ITMO_FS.filters.multivariate")
_add(B.StandaloneSelector, kwargs=dict(n_features=10), factory=_f_stir,
     name="STIR", display="STIR", family="filters.multivariate",
     component_type="standalone_selector", summary="Seleção via algoritmo STIR (baseado em vizinhança).",
     itmo_symbol="STIR", itmo_signature="STIR(n_features_to_keep).fit(X,y).transform(X)",
     status="OK", recommends_scaling="standard", params={"n_features": "nº de features a manter"},
     outputs_scores=True, references="ITMO_FS.filters.multivariate")
_add(B.StandaloneSelector, kwargs=dict(n_features=10), factory=_f_trf,
     name="TraceRatioFisher", display="Trace Ratio (Fisher)", family="filters.multivariate",
     component_type="standalone_selector",
     summary="Trace Ratio supervisionado (versão Fisher, baseado em similaridade).",
     itmo_symbol="TraceRatioFisher", itmo_signature="TraceRatioFisher(n_selected).fit(X,y).transform(X)",
     status="OK", recommends_scaling="standard", params={"n_features": "nº de features"},
     outputs_scores=True, references="ITMO_FS.filters.multivariate")

# MIMAGA — presente; custoso/estocástico -> catalogado como broken-por-padrão (habilitável)
_add(B.BrokenMethod, name="MIMAGA", display="MIMAGA", family="filters.multivariate",
     component_type="standalone_selector", summary="MIM + algoritmo genético (estocástico, custoso).",
     itmo_symbol="MIMAGA", itmo_signature="MIMAGA(mim_size, pop_size, max_iter, f_target, k1..k4)",
     status="BROKEN_IN_0_3_3", quirks="requer muitos hiperparâmetros e é estocástico; não incluído por padrão.")

# ============================================================ ESPARSOS/NÃO SUPERVISIONADOS
def _f_mcfs(p): return I.MCFS(d=p.get("n_features", 10), scheme="0-1")
def _f_udfs(p): return I.UDFS(p=p.get("n_features", 10))
def _f_ndfs(p): return I.NDFS(p=p.get("n_features", 10))
def _f_rfs(p): return I.RFS(p=p.get("n_features", 10))
def _f_spec(p): return I.SPEC(p=p.get("n_features", 10), phi_type=1)
def _f_trl(p): return I.TraceRatioLaplacian(n_selected_features=p.get("n_features", 10))

_sparse = [
    ("MCFS", "MCFS", "Unsupervised FS for Multi-Cluster Data.", _f_mcfs, "unsupervised", "not_used",
     "scheme='dot' é bugado; usamos '0-1'."),
    ("UDFS", "UDFS", "Unsupervised Discriminative Feature Selection.", _f_udfs, "unsupervised", "not_used", ""),
    ("NDFS", "NDFS", "Nonnegative Discriminative Feature Selection.", _f_ndfs, "unsupervised", "not_used", ""),
    ("RFS", "RFS", "Robust Feature Selection (L2,1-norms).", _f_rfs, "label_aware", "required", ""),
    ("SPEC", "SPEC", "Spectral Feature Selection.", _f_spec, "label_aware", "optional",
     "modo não supervisionado (y=None) é bugado; use label_aware."),
    ("TraceRatioLaplacian", "Trace Ratio (Laplacian)", "Trace Ratio não supervisionado (Laplacian).",
     _f_trl, "label_aware", "optional", "run() retorna (indices, score, lambda)."),
]
for name, disp, summ, fac, mode, yreq, quirk in _sparse:
    fam = "filters.sparse" if name in ("MCFS", "UDFS", "NDFS", "RFS", "SPEC") else "filters.unsupervised"
    _add(B.SparseSelector, kwargs=dict(n_features=10, mode=mode), factory=fac,
         name=name, display=disp, family=fam, component_type="standalone_selector",
         summary=summ, itmo_symbol=name,
         itmo_signature=f"{name}(...).run(X[, y]); feature_ranking(W)", status="OK_WITH_ADAPTER",
         y=yreq, recommends_scaling="standard",
         params={"n_features": "nº de features (top do ranking)",
                 "mode": "unsupervised | label_aware"},
         outputs_scores=False, outputs_ranking=True, outputs_subset=True,
         quirks=quirk, references=f"ITMO_FS.{fam}")

# ============================================================ ENSEMBLES
_add(B.WeightBasedEnsemble, kwargs=dict(base_measures=["GiniIndex", "FRatio", "SpearmanCorr"], k=10),
     name="WeightBased", display="WeightBased", family="ensembles.measure_based",
     component_type="ensemble_selector",
     summary="Ensemble por fusão de SCORES normalizados de filtros base.",
     itmo_symbol="WeightBased", itmo_signature="WeightBased(filters).fit(X,y); transform(X, cutting_rule[, fusion, weights])",
     status="OK", y="required",
     params={"base_measures": "lista de medidas (strings do UnivariateFilter)",
             "k": "nº de features (cutting rule)", "cutting_rule": "regra de corte",
             "weights": "pesos por filtro (None=uniforme)"},
     outputs_scores=True, quirks="normalização min-max por base pode apagar correlação negativa (harmonize a direção).",
     example=">>> get('WeightBased', base_measures=['GiniIndex','FRatio'], k=10).fit(X,y)",
     references="ITMO_FS.ensembles.measure_based")
_add(B.MixedEnsemble, kwargs=dict(base_measures=["spearman_corr", "pearson_corr", "f_ratio_measure"], k=10),
     name="Mixed", display="Mixed", family="ensembles.ranking_based",
     component_type="ensemble_selector", summary="Ensemble por fusão de RANKINGS (robusto à escala).",
     itmo_symbol="Mixed", itmo_signature="Mixed(filter_functions).fit(X,y); transform(X, k[, fusion])",
     status="OK", y="required", outputs_scores=False,
     params={"base_measures": "lista de FUNÇÕES de medida", "k": "nº de features"},
     quirks="bases são funções de medida (não objetos filtro).",
     references="ITMO_FS.ensembles.ranking_based")
_add(B.BestSumEnsemble, kwargs=dict(base_measures=["GiniIndex", "FRatio"], k=10, k_each=8),
     name="BestSum", display="BestSum", family="ensembles.model_based",
     component_type="ensemble_selector",
     summary="Ensemble model-based: importâncias ponderadas por desempenho de CV (só treino).",
     itmo_symbol="BestSum", itmo_signature="BestSum(models, cutting_rule).fit(X,y); cut()",
     status="OK_WITH_ADAPTER", y="required", outputs_scores=True, recommends_scaling="standard",
     params={"base_measures": "medidas base (via adaptador com selected_features+best_score)",
             "k": "nº de features", "k_each": "nº de features por modelo base"},
     quirks="BestSum marcado 'not stable'; predict() é bugado — usamos fit()+cut().",
     references="ITMO_FS.ensembles.model_based")

# ============================================================ HÍBRIDOS
_add(B.MelifHybrid, kwargs=dict(base_measures=["GiniIndex", "FRatio"], k=10),
     name="Melif", display="Melif", family="hybrid", component_type="hybrid_selector",
     summary="Otimiza pesos de um ensemble de filtros para maximizar um scorer (só treino).",
     itmo_symbol="Melif", itmo_signature="Melif(filter_ensemble, scorer).fit(X,y,estimator,cutting_rule)",
     status="OK", y="required", recommends_scaling="standard",
     params={"base_measures": "medidas do ensemble base", "k": "nº de features",
             "estimator": "classificador (default LogisticRegression)",
             "scorer": "função scorer(y_true,y_pred) (default f1_macro)"},
     outputs_scores=False, quirks="scorer é obrigatório (default fornecido pelo itmofs-lab).",
     references="ITMO_FS.hybrid")
_add(B.BrokenMethod, name="FilterWrapperHybrid", display="Filter+Wrapper Hybrid", family="hybrid",
     component_type="hybrid_selector", summary="Filtro rápido seguido de wrapper.",
     itmo_symbol="FilterWrapperHybrid", itmo_signature="FilterWrapperHybrid(filter_, wrapper).fit(X,y)",
     status="BROKEN_IN_0_3_3", quirks="usa RecursiveElimination internamente (bug list.remove em ndarray).")

# ============================================================ EMBEDDED
def _f_mos(p): return I.MOS(loss="hinge")
_add(B.StandaloneSelector, kwargs=dict(supervised=True), factory=_f_mos,
     name="MOS", display="MOS / MOSS / MOSNS", family="embedded", component_type="embedded_selector",
     summary="Minimizing Overlapping Selection (com/sem SMOTE) via modelo linear regularizado.",
     itmo_symbol="MOS", itmo_signature="MOS(model, loss, seed).fit(X,y).transform(X)",
     status="OK", y="required", recommends_scaling="standard",
     params={"(interno)": "usa loss='hinge' (loss='log' foi removido no sklearn atual)"},
     outputs_scores=False, quirks="loss='log' quebrado no sklearn atual; itmofs-lab usa 'hinge'.",
     references="ITMO_FS.embedded")

# ============================================================ WRAPPERS
_add(B.WrapperSelector, kwargs=dict(n_features=10),
     name="BackwardSelection", display="Backward Selection", family="wrappers",
     component_type="wrapper_selector", summary="Remove uma feature por vez até atingir n_features.",
     itmo_symbol="BackwardSelection", itmo_signature="BackwardSelection(estimator, n_features, measure).fit(X,y)",
     status="OK", y="required", recommends_scaling="standard",
     params={"estimator": "classificador sklearn (default LogisticRegression)",
             "n_features": "nº de features finais", "measure": "score(y_true,y_pred) (default accuracy)"},
     outputs_scores=False, references="ITMO_FS.wrappers.deterministic")
_add(B.WrapperSelector, kwargs=dict(n_features=10),
     name="SequentialForwardSelection", display="Sequential Forward Selection", family="wrappers",
     component_type="wrapper_selector", summary="Adiciona sequencialmente a feature que mais melhora o classificador.",
     itmo_symbol="SequentialForwardSelection",
     itmo_signature="SequentialForwardSelection(estimator, n_features, measure).fit(X,y)",
     status="OK", y="required", recommends_scaling="standard",
     params={"estimator": "classificador sklearn", "n_features": "nº de features", "measure": "score"},
     outputs_scores=False, references="ITMO_FS.wrappers.deterministic")
for nm, disp, sig, q in [
    ("RecursiveElimination", "Recursive Elimination", "RecursiveElimination(estimator, n_features).fit(X,y)",
     "bug: list.remove em ndarray -> AttributeError."),
    ("AddDelWrapper", "Add-Del Wrapper", "AddDelWrapper(estimator, score, maximize, seed).fit(X,y)",
     "bug: score chamado como int -> TypeError."),
    ("HillClimbingWrapper", "Hill Climbing", "HillClimbingWrapper(estimator, scorer).fit(X,y)",
     "bug: compara dict com int -> TypeError."),
    ("SimulatedAnnealing", "Simulated Annealing", "SimulatedAnnealing(classifier, score, ...).fit(X,y,test_x,test_y)",
     "fit exige dados de teste (leakage por design)."),
    ("TPhMGWO", "Two-Phase Mutation GWO", "TPhMGWO(...).run(X,y)",
     "usa np.float (removido no numpy>=1.24) -> AttributeError."),
]:
    st = "LEAKAGE_BY_DESIGN" if nm == "SimulatedAnnealing" else "BROKEN_IN_0_3_3"
    _add(B.BrokenMethod, name=nm, display=disp, family="wrappers",
         component_type="wrapper_selector", summary="Wrapper baseado em busca guiada por classificador.",
         itmo_symbol=nm, itmo_signature=sig, status=st, y="required", outputs_scores=False, quirks=q)

# ============================================================ APOIO
_add(B.SupportComponent, name="VDM", display="Value Difference Metric", family="filters.univariate",
     component_type="support_metric", summary="Métrica de diferença de valores categóricos condicionada às classes.",
     itmo_symbol="VDM", itmo_signature="VDM(weighted).run(X, y) -> matriz de distância",
     status="SUPPORT_ONLY", y="required", outputs_scores=False, outputs_ranking=False,
     outputs_subset=False, transforms_test=False,
     quirks="não seleciona features; apoia métodos baseados em distância.",
     references="ITMO_FS.filters.univariate")
