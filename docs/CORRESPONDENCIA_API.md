# Correspondência com a API ITMO_FS

Este documento reconcilia os métodos do **itmofs-lab** com a API oficial da
**ITMO_FS**. Ponto-chave: o itmofs-lab cataloga a **instalação real (0.3.3)**,
que é um **superconjunto** da documentação pública da 0.3.2. Por isso alguns
métodos existem na biblioteca e não aparecem nos docs antigos — não são erros.

## Pontos de atenção (do de-para) e resolução

| símbolo | itmofs-lab | API 0.3.2 (docs) | explicação | resolução |
|---|---|---|---|---|
| `anova` | ✅ tem | 🆕 não lista | existe no runtime **0.3.3** (`filters.univariate.measures`) | mantido; anotado como *presente na 0.3.3* |
| `laplacian_score` | ✅ tem | 🆕 não lista | existe no runtime **0.3.3** (`filters.univariate.measures`); não supervisionado | mantido; anotado como *presente na 0.3.3* |
| `qpfs_filter` / `qpfs_wrapper` | tinha só `qpfs_filter` | lista `qpfs_wrapper` | são **dois símbolos distintos e reais**: `qpfs_filter` é medida univariada; `qpfs_wrapper` é wrapper `(X, y, alpha, …)` | **adicionado `qpfs_wrapper`**; agora a lib cobre os dois (ambos exigem solver de QP, ausente → `DEPENDENCY_MISSING`) |

Com o `qpfs_wrapper` adicionado, o itmofs-lab passa a cobrir **100%** dos
símbolos da API 0.3.2, mais os extras da 0.3.3 (`anova`, `laplacian_score`).

## Tabela completa (52 métodos catalogados)

Status: 🟢 executa · 🟢(ad) via adaptador · 🟠 dependência ausente · 🔴 indisponível na 0.3.3 · ⚪ apoio

| # | símbolo (itmofs-lab) | família | status |
|---:|---|---|---|
| 1 | `AddDelWrapper` | wrappers | 🔴 BROKEN_IN_0_3_3 |
| 2 | `BackwardSelection` | wrappers | 🟢 OK |
| 3 | `BestSum` | ensembles.model_based | 🟢(ad) OK_WITH_ADAPTER |
| 4 | `CFR` | filters.multivariate | 🟢 OK |
| 5 | `CIFE` | filters.multivariate | 🟢 OK |
| 6 | `CMIM` | filters.multivariate | 🟢 OK |
| 7 | `DCSF` | filters.multivariate | 🟢 OK |
| 8 | `DISRWithMassive` | filters.multivariate | 🟢 OK |
| 9 | `FCBFDiscreteFilter` | filters.multivariate | 🟢 OK |
| 10 | `FilterWrapperHybrid` | hybrid | 🔴 BROKEN_IN_0_3_3 |
| 11 | `HillClimbingWrapper` | wrappers | 🔴 BROKEN_IN_0_3_3 |
| 12 | `ICAP` | filters.multivariate | 🟢 OK |
| 13 | `IWFS` | filters.multivariate | 🟢 OK |
| 14 | `JMI` | filters.multivariate | 🟢 OK |
| 15 | `MCFS` | filters.sparse | 🟢(ad) OK_WITH_ADAPTER |
| 16 | `MIFS` | filters.multivariate | 🟢 OK |
| 17 | `MIM` | filters.multivariate | 🟢 OK |
| 18 | `MIMAGA` | filters.multivariate | 🔴 BROKEN_IN_0_3_3 |
| 19 | `MOS` | embedded | 🟢 OK |
| 20 | `MRI` | filters.multivariate | 🟢 OK |
| 21 | `MRMR` | filters.multivariate | 🟢 OK |
| 22 | `Melif` | hybrid | 🟢 OK |
| 23 | `Mixed` | ensembles.ranking_based | 🟢 OK |
| 24 | `NDFS` | filters.sparse | 🟢(ad) OK_WITH_ADAPTER |
| 25 | `RFS` | filters.sparse | 🟢(ad) OK_WITH_ADAPTER |
| 26 | `RecursiveElimination` | wrappers | 🔴 BROKEN_IN_0_3_3 |
| 27 | `SPEC` | filters.sparse | 🟢(ad) OK_WITH_ADAPTER |
| 28 | `STIR` | filters.multivariate | 🟢 OK |
| 29 | `SequentialForwardSelection` | wrappers | 🟢 OK |
| 30 | `SimulatedAnnealing` | wrappers | 🔴 LEAKAGE_BY_DESIGN |
| 31 | `TPhMGWO` | wrappers | 🔴 BROKEN_IN_0_3_3 |
| 32 | `TraceRatioFisher` | filters.multivariate | 🟢 OK |
| 33 | `TraceRatioLaplacian` | filters.unsupervised | 🟢(ad) OK_WITH_ADAPTER |
| 34 | `UDFS` | filters.sparse | 🟢(ad) OK_WITH_ADAPTER |
| 35 | `VDM` | filters.univariate | ⚪ SUPPORT_ONLY |
| 36 | `WeightBased` | ensembles.measure_based | 🟢 OK |
| 37 | `anova` | filters.univariate | 🟢 OK |
| 38 | `chi2_measure` | filters.univariate | 🟢 OK |
| 39 | `f_ratio_measure` | filters.univariate | 🟢 OK |
| 40 | `fechner_corr` | filters.univariate | 🟢 OK |
| 41 | `fit_criterion_measure` | filters.univariate | 🔴 BROKEN_IN_0_3_3 |
| 42 | `generalizedCriteria` | filters.multivariate | 🟢 OK |
| 43 | `gini_index` | filters.univariate | 🟢 OK |
| 44 | `information_gain` | filters.univariate | 🟢 OK |
| 45 | `kendall_corr` | filters.univariate | 🟢 OK |
| 46 | `laplacian_score` | filters.univariate | 🟢 OK |
| 47 | `pearson_corr` | filters.univariate | 🟢 OK |
| 48 | `qpfs_filter` | filters.univariate | 🟠 DEPENDENCY_MISSING |
| 49 | `qpfs_wrapper` | wrappers | 🟠 DEPENDENCY_MISSING |
| 50 | `reliefF_measure` | filters.univariate | 🟢 OK |
| 51 | `spearman_corr` | filters.univariate | 🟢 OK |
| 52 | `su_measure` | filters.univariate | 🟢 OK |
