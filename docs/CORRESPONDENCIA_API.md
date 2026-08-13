# Correspondência com a API ITMO_FS

Reconciliação **completa (nos dois sentidos)** entre o `itmofs-lab` e a API da
ITMO_FS. O `itmofs-lab` cataloga a **instalação real (0.3.3)**, um **superconjunto**
dos docs públicos da 0.3.2. **Todo símbolo público** está classificado abaixo — como
**método**, **interface**, **regra de corte** ou **apoio/utilitário**. Nada fica sem rótulo.

## 1. Pontos de atenção do de-para (resolvidos)

| símbolo | itmofs-lab | API 0.3.2 | explicação | resolução |
|---|---|---|---|---|
| `anova` | ✅ tem | 🆕 não lista | existe no runtime **0.3.3** (`filters.univariate.measures`) | mantido; anotado *presente na 0.3.3* |
| `laplacian_score` | ✅ tem | 🆕 não lista | existe no runtime **0.3.3**; não supervisionado | mantido; anotado *presente na 0.3.3* |
| `qpfs_filter` / `qpfs_wrapper` | só tinha `qpfs_filter` | lista `qpfs_wrapper` | dois símbolos distintos (medida vs wrapper) | **adicionado `qpfs_wrapper`** — cobre os dois |

## 2. Métodos expostos pelo itmofs-lab (52)

Cada um usável com `fs.get('<nome>')` e `itmofs-lab info <nome>`.

| símbolo | família | tipo | status |
|---|---|---|---|
| `AddDelWrapper` | wrappers | wrapper_selector | 🔴 `BROKEN_IN_0_3_3` |
| `BackwardSelection` | wrappers | wrapper_selector | 🟢 `OK` |
| `BestSum` | ensembles.model_based | ensemble_selector | 🟢(adaptador) `OK_WITH_ADAPTER` |
| `CFR` | filters.multivariate | criterion_function | 🟢 `OK` |
| `CIFE` | filters.multivariate | criterion_function | 🟢 `OK` |
| `CMIM` | filters.multivariate | criterion_function | 🟢 `OK` |
| `DCSF` | filters.multivariate | criterion_function | 🟢 `OK` |
| `DISRWithMassive` | filters.multivariate | standalone_selector | 🟢 `OK` |
| `FCBFDiscreteFilter` | filters.multivariate | standalone_selector | 🟢 `OK` |
| `FilterWrapperHybrid` | hybrid | hybrid_selector | 🔴 `BROKEN_IN_0_3_3` |
| `HillClimbingWrapper` | wrappers | wrapper_selector | 🔴 `BROKEN_IN_0_3_3` |
| `ICAP` | filters.multivariate | criterion_function | 🟢 `OK` |
| `IWFS` | filters.multivariate | criterion_function | 🟢 `OK` |
| `JMI` | filters.multivariate | criterion_function | 🟢 `OK` |
| `MCFS` | filters.sparse | standalone_selector | 🟢(adaptador) `OK_WITH_ADAPTER` |
| `MIFS` | filters.multivariate | criterion_function | 🟢 `OK` |
| `MIM` | filters.multivariate | criterion_function | 🟢 `OK` |
| `MIMAGA` | filters.multivariate | standalone_selector | 🔴 `BROKEN_IN_0_3_3` |
| `MOS` | embedded | embedded_selector | 🟢 `OK` |
| `MRI` | filters.multivariate | criterion_function | 🟢 `OK` |
| `MRMR` | filters.multivariate | criterion_function | 🟢 `OK` |
| `Melif` | hybrid | hybrid_selector | 🟢 `OK` |
| `Mixed` | ensembles.ranking_based | ensemble_selector | 🟢 `OK` |
| `NDFS` | filters.sparse | standalone_selector | 🟢(adaptador) `OK_WITH_ADAPTER` |
| `RFS` | filters.sparse | standalone_selector | 🟢(adaptador) `OK_WITH_ADAPTER` |
| `RecursiveElimination` | wrappers | wrapper_selector | 🔴 `BROKEN_IN_0_3_3` |
| `SPEC` | filters.sparse | standalone_selector | 🟢(adaptador) `OK_WITH_ADAPTER` |
| `STIR` | filters.multivariate | standalone_selector | 🟢 `OK` |
| `SequentialForwardSelection` | wrappers | wrapper_selector | 🟢 `OK` |
| `SimulatedAnnealing` | wrappers | wrapper_selector | 🔴 `LEAKAGE_BY_DESIGN` |
| `TPhMGWO` | wrappers | wrapper_selector | 🔴 `BROKEN_IN_0_3_3` |
| `TraceRatioFisher` | filters.multivariate | standalone_selector | 🟢 `OK` |
| `TraceRatioLaplacian` | filters.unsupervised | standalone_selector | 🟢(adaptador) `OK_WITH_ADAPTER` |
| `UDFS` | filters.sparse | standalone_selector | 🟢(adaptador) `OK_WITH_ADAPTER` |
| `VDM` | filters.univariate | support_metric | ⚪ `SUPPORT_ONLY` |
| `WeightBased` | ensembles.measure_based | ensemble_selector | 🟢 `OK` |
| `anova` | filters.univariate | score_function | 🟢 `OK` |
| `chi2_measure` | filters.univariate | score_function | 🟢 `OK` |
| `f_ratio_measure` | filters.univariate | score_function | 🟢 `OK` |
| `fechner_corr` | filters.univariate | score_function | 🟢 `OK` |
| `fit_criterion_measure` | filters.univariate | score_function | 🔴 `BROKEN_IN_0_3_3` |
| `generalizedCriteria` | filters.multivariate | criterion_function | 🟢 `OK` |
| `gini_index` | filters.univariate | score_function | 🟢 `OK` |
| `information_gain` | filters.univariate | score_function | 🟢 `OK` |
| `kendall_corr` | filters.univariate | score_function | 🟢 `OK` |
| `laplacian_score` | filters.univariate | score_function | 🟢 `OK` |
| `pearson_corr` | filters.univariate | score_function | 🟢 `OK` |
| `qpfs_filter` | filters.univariate | score_function | 🟠 `DEPENDENCY_MISSING` |
| `qpfs_wrapper` | wrappers | wrapper_selector | 🟠 `DEPENDENCY_MISSING` |
| `reliefF_measure` | filters.univariate | score_function | 🟢 `OK` |
| `spearman_corr` | filters.univariate | score_function | 🟢 `OK` |
| `su_measure` | filters.univariate | score_function | 🟢 `OK` |

## 3. Interfaces internas (2)

São os *motores* que o `itmofs-lab` usa por baixo dos panos; você normalmente não
os instancia diretamente — usa `fs.get(...)`.

| interface | papel |
|---|---|
| `UnivariateFilter` | aplica uma medida univariada + regra de corte (usada por todos os filtros univariados) |
| `MultivariateFilter` | seleção sequencial por critério (usada por MRMR, JMI, CMIM, …) |

## 4. Regras de corte (6) — usadas como parâmetro

Convertem scores em índices; entram via `cutting_rule=`/`k=` (ex.: `fs.get('gini_index', cutting_rule='select_best_percentage', cutting_param=0.2)`).

| regra | assinatura |
|---|---|
| `select_best_by_value` | `select_best_by_value(value)` |
| `select_best_percentage` | `select_best_percentage(percent)` |
| `select_k_best` | `select_k_best(k)` |
| `select_k_worst` | `select_k_worst(k)` |
| `select_worst_by_value` | `select_worst_by_value(value)` |
| `select_worst_percentage` | `select_worst_percentage(percent)` |

## 5. Componentes de apoio / utilitários (32)

Não selecionam features; sustentam os métodos (fusão, teoria da informação, validação, álgebra).

- **Funções de fusão (ensembles):** `best_goes_first_fusion`, `borda_fusion`, `weight_fusion`
- **Teoria da informação:** `builder_dict`, `conditional_entropy`, `conditional_mutual_information`, `elog`, `entropy`, `interaction_information`, `joint_mutual_information`, `matrix_mutual_information`, `mutual_information`
- **Registros de medidas:** `GLOB_MEASURE`, `RESTRICTIONS`
- **Validadores / verificações:** `DataChecker`, `check_classifier`, `check_cutting_rule`, `check_data`, `check_features`, `check_filters`, `check_restrictions`, `check_scorer`, `check_shapes`, `generate_features`
- **Utilitários numéricos:** `augmented_rvalue`, `cartesian`, `knn`, `l21_norm`, `matrix_norm`, `normalize`, `power_neg_half`, `qpfs_body`

---

**Fechamento:** 52 métodos + 2 interfaces + 6 regras de corte + 32 apoios = **92 símbolos classificados** — cobertura de 100% da API pública.