# Catálogo de métodos

Documentação completa de todos os métodos da ITMO_FS acessíveis pelo itmofs-lab, com **o que entra** e **o que sai** de cada um.

## Embedded  (`embedded`)

| método | status | resumo |
|---|---|---|
| [`MOS`](methods/MOS.md) | `OK` | Minimizing Overlapping Selection (com/sem SMOTE) via modelo linear regularizado. |

## Ensembles (baseados em medida)  (`ensembles.measure_based`)

| método | status | resumo |
|---|---|---|
| [`WeightBased`](methods/WeightBased.md) | `OK` | Ensemble por fusão de SCORES normalizados de filtros base. |

## Ensembles (baseados em modelo)  (`ensembles.model_based`)

| método | status | resumo |
|---|---|---|
| [`BestSum`](methods/BestSum.md) | `OK_WITH_ADAPTER` | Ensemble model-based: importâncias ponderadas por desempenho de CV (só treino). |

## Ensembles (baseados em ranking)  (`ensembles.ranking_based`)

| método | status | resumo |
|---|---|---|
| [`Mixed`](methods/Mixed.md) | `OK` | Ensemble por fusão de RANKINGS (robusto à escala). |

## Filtros multivariados  (`filters.multivariate`)

| método | status | resumo |
|---|---|---|
| [`CFR`](methods/CFR.md) | `OK` | Maximiza correlação e minimiza redundância. |
| [`CIFE`](methods/CIFE.md) | `OK` | Conditional Infomax Feature Extraction. |
| [`CMIM`](methods/CMIM.md) | `OK` | Conditional Mutual Info Maximisation. |
| [`DCSF`](methods/DCSF.md) | `OK` | Dynamic change of selected feature. |
| [`DISRWithMassive`](methods/DISRWithMassive.md) | `OK` | Double Input Symmetric Relevance (kASSI); maximiza info mútua evitando densidade multivariada grande. |
| [`FCBFDiscreteFilter`](methods/FCBFDiscreteFilter.md) | `OK` | Fast Correlation Based Filter para dados discretos (info mútua; remove redundância). |
| [`ICAP`](methods/ICAP.md) | `OK` | Interaction Capping. |
| [`IWFS`](methods/IWFS.md) | `OK` | Interaction Weight based feature scoring. |
| [`JMI`](methods/JMI.md) | `OK` | Informação mútua conjunta (complementaridade). |
| [`MIFS`](methods/MIFS.md) | `OK` | Relevância menos penalização de redundância (parâmetro beta). |
| [`MIM`](methods/MIM.md) | `OK` | Maximiza relevância (informação mútua) com o alvo. |
| [`MIMAGA`](methods/MIMAGA.md) | `BROKEN_IN_0_3_3` | MIM + algoritmo genético (estocástico, custoso). |
| [`MRI`](methods/MRI.md) | `OK` | Max-Relevance and Max-Independence. |
| [`MRMR`](methods/MRMR.md) | `OK` | Máxima relevância e mínima redundância. |
| [`STIR`](methods/STIR.md) | `OK` | Seleção via algoritmo STIR (baseado em vizinhança). |
| [`TraceRatioFisher`](methods/TraceRatioFisher.md) | `OK` | Trace Ratio supervisionado (versão Fisher, baseado em similaridade). |
| [`generalizedCriteria`](methods/generalizedCriteria.md) | `OK` | Combinação linear de relevância/redundância/dependência (beta, gamma). |

## Filtros esparsos  (`filters.sparse`)

| método | status | resumo |
|---|---|---|
| [`MCFS`](methods/MCFS.md) | `OK_WITH_ADAPTER` | Unsupervised FS for Multi-Cluster Data. |
| [`NDFS`](methods/NDFS.md) | `OK_WITH_ADAPTER` | Nonnegative Discriminative Feature Selection. |
| [`RFS`](methods/RFS.md) | `OK_WITH_ADAPTER` | Robust Feature Selection (L2,1-norms). |
| [`SPEC`](methods/SPEC.md) | `OK_WITH_ADAPTER` | Spectral Feature Selection. |
| [`UDFS`](methods/UDFS.md) | `OK_WITH_ADAPTER` | Unsupervised Discriminative Feature Selection. |

## Filtros univariados  (`filters.univariate`)

| método | status | resumo |
|---|---|---|
| [`VDM`](methods/VDM.md) | `SUPPORT_ONLY` | Métrica de diferença de valores categóricos condicionada às classes. |
| [`anova`](methods/anova.md) | `OK` | Estatística F de ANOVA por feature. |
| [`chi2_measure`](methods/chi2_measure.md) | `OK` | Estatística qui-quadrado entre feature e classe. |
| [`f_ratio_measure`](methods/f_ratio_measure.md) | `OK` | Calcula o Fisher score de cada feature (separação entre classes). |
| [`fechner_corr`](methods/fechner_corr.md) | `OK` | Correlação de sinal (Fechner) de cada feature. |
| [`fit_criterion_measure`](methods/fit_criterion_measure.md) | `BROKEN_IN_0_3_3` | Critério de ajuste por classe (centros/variâncias). |
| [`gini_index`](methods/gini_index.md) | `OK` | Índice de Gini: medida de dispersão estatística por feature. |
| [`information_gain`](methods/information_gain.md) | `OK` | Informação mútua I(X;Y)=H(X)-H(X|Y) por feature. |
| [`kendall_corr`](methods/kendall_corr.md) | `OK` | Correlação de sinal (Kendall) de cada feature. |
| [`laplacian_score`](methods/laplacian_score.md) | `OK` | Score laplaciano (não supervisionado); menor é melhor. |
| [`pearson_corr`](methods/pearson_corr.md) | `OK` | Correlação de Pearson de cada feature com o alvo. |
| [`qpfs_filter`](methods/qpfs_filter.md) | `DEPENDENCY_MISSING` | Quadratic Programming Feature Selection. |
| [`reliefF_measure`](methods/reliefF_measure.md) | `OK` | Medida ReliefF baseada em vizinhos mais próximos. |
| [`spearman_corr`](methods/spearman_corr.md) | `OK` | Correlação de Spearman de cada feature com o alvo. |
| [`su_measure`](methods/su_measure.md) | `OK` | Correlação informacional SU(X,Y)=2*I(X;Y)/(H(X)+H(Y)). |

## Filtros não supervisionados  (`filters.unsupervised`)

| método | status | resumo |
|---|---|---|
| [`TraceRatioLaplacian`](methods/TraceRatioLaplacian.md) | `OK_WITH_ADAPTER` | Trace Ratio não supervisionado (Laplacian). |

## Híbridos  (`hybrid`)

| método | status | resumo |
|---|---|---|
| [`FilterWrapperHybrid`](methods/FilterWrapperHybrid.md) | `BROKEN_IN_0_3_3` | Filtro rápido seguido de wrapper. |
| [`Melif`](methods/Melif.md) | `OK` | Otimiza pesos de um ensemble de filtros para maximizar um scorer (só treino). |

## Wrappers  (`wrappers`)

| método | status | resumo |
|---|---|---|
| [`AddDelWrapper`](methods/AddDelWrapper.md) | `BROKEN_IN_0_3_3` | Wrapper baseado em busca guiada por classificador. |
| [`BackwardSelection`](methods/BackwardSelection.md) | `OK` | Remove uma feature por vez até atingir n_features. |
| [`HillClimbingWrapper`](methods/HillClimbingWrapper.md) | `BROKEN_IN_0_3_3` | Wrapper baseado em busca guiada por classificador. |
| [`RecursiveElimination`](methods/RecursiveElimination.md) | `BROKEN_IN_0_3_3` | Wrapper baseado em busca guiada por classificador. |
| [`SequentialForwardSelection`](methods/SequentialForwardSelection.md) | `OK` | Adiciona sequencialmente a feature que mais melhora o classificador. |
| [`SimulatedAnnealing`](methods/SimulatedAnnealing.md) | `LEAKAGE_BY_DESIGN` | Wrapper baseado em busca guiada por classificador. |
| [`TPhMGWO`](methods/TPhMGWO.md) | `BROKEN_IN_0_3_3` | Wrapper baseado em busca guiada por classificador. |
| [`qpfs_wrapper`](methods/qpfs_wrapper.md) | `DEPENDENCY_MISSING` | Quadratic Programming Feature Selection na forma de wrapper. |
