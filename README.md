<h1 align="center">itmofs-lab</h1>

<p align="center">
  <strong>Uma interface simples, uniforme e honesta para seleção de características com a
  <a href="https://github.com/ctlab/ITMO_FS">ITMO_FS</a>.</strong><br>
  Todos os métodos com a mesma API, um comando de ajuda que mostra <em>o que entra e o que sai</em>,
  e a documentação completa de cada método aqui no README.
</p>

<p align="center">
  <a href="https://pypi.org/project/itmofs-lab/"><img alt="PyPI" src="https://img.shields.io/pypi/v/itmofs-lab?color=blue&label=PyPI"></a>
  <img alt="Python" src="https://img.shields.io/pypi/pyversions/itmofs-lab">
  <img alt="License" src="https://img.shields.io/pypi/l/itmofs-lab?color=green">
  <img alt="Downloads" src="https://img.shields.io/pypi/dm/itmofs-lab?color=orange">
  <img alt="Status" src="https://img.shields.io/badge/status-ativo-brightgreen">
</p>

<p align="center">
  <code>pip install itmofs-lab</code>
</p>

---

## Por que existe

A [ITMO_FS](https://github.com/ctlab/ITMO_FS) reúne dezenas de métodos de
**feature selection** (filtros, ensembles, wrappers), mas com uma API
heterogênea: algumas medidas são funções, outras são classes; umas usam
`fit/transform`, outras `run/feature_ranking`; as regras de corte operam sobre
dicionários; e há bugs e requisitos que só aparecem em tempo de execução.

O **itmofs-lab** entrega tudo isso com uma cara só:

- ✅ **API única** — todo método usa `fit` / `transform` e expõe `selected_`,
  `selected_names_` e `scores_`.
- ✅ **Comando de ajuda** — `itmofs-lab info <método>` (ou `m.info()`) mostra
  exatamente **o que entra e o que sai**.
- ✅ **Um arquivo por método**, importável isoladamente.
- ✅ **Honestidade** — métodos que não executam na versão instalada ficam
  documentados e levantam um erro claro em vez de falhar de forma obscura.
- ✅ **Rigor científico** — pensado para que o conjunto de teste **nunca**
  participe da seleção.

## Instalação

```bash
pip install itmofs-lab
```

> **⚠️ Recomendação de ambiente.** A ITMO_FS 0.3.3 é de ~2021. Para os métodos
> rodarem sem erros de runtime, use dependências compatíveis:
>
> ```bash
> pip install "numpy<2" "pandas<2" "scikit-learn<1.4" itmofs-lab
> ```

## Uso em 30 segundos

```python
import itmofs_lab as fs
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, stratify=y, random_state=42)

m = fs.get("gini_index", k=10)      # escolha o método pelo nome
m.fit(X_tr, y_tr)                   # ajusta SÓ no treino (anti-leakage)
X_te_sel = m.transform(X_te)        # aplica as mesmas colunas ao teste

print(m.selected_)                  # índices selecionados
print(m.selected_names_)            # nomes das features
print(m.scores_)                    # scores por feature (ou None)
```

## Comando de ajuda: o que entra e o que sai

```bash
itmofs-lab list                     # todos os métodos + status
itmofs-lab families                 # métodos agrupados por família
itmofs-lab info gini_index          # o que entra e o que sai deste método
itmofs-lab run gini_index --dataset breast_cancer -k 10
itmofs-lab version
```

No Python: `fs.info("gini_index")`, `fs.list_methods(family="ensembles")`,
`fs.get("chi2_measure").info()`.

## Um arquivo por método

```python
from itmofs_lab.filters.univariate.gini_index import GiniIndex
from itmofs_lab.ensembles.WeightBased import WeightBased

m = GiniIndex(k=10)                 # equivalente a fs.get("gini_index", k=10)
print(GiniIndex.info())
```

## Regra científica: anti-leakage

```text
dataset → split treino/teste → preprocessing.fit(treino) → seletor.fit(treino)
        → transform(treino) e transform(teste) → classificador → avaliação no teste
```

O conjunto de **teste nunca** participa da seleção. Chame `fit` apenas com
`X_train` (e `y_train` quando supervisionado), aplique `transform` ao teste
depois, e escolha `k`/threshold **somente** por validação cruzada no treino.

## 📚 Documentação completa dos métodos

> **52 métodos** catalogados e documentados.

Cobertura de **todas as famílias** da ITMO_FS. Clique para ir à seção:

- **[🔹 Filtros univariados](#🔹 filtros univariados)** — 15 método(s)
- **[🔸 Filtros multivariados](#🔸 filtros multivariados)** — 17 método(s)
- **[🌐 Filtros esparsos](#🌐 filtros esparsos)** — 5 método(s)
- **[🧩 Filtros não supervisionados](#🧩 filtros não supervisionados)** — 1 método(s)
- **[🧠 Ensemble — baseado em medidas (WeightBased)](#🧠 ensemble — baseado em medidas (weightbased))** — 1 método(s)
- **[🧠 Ensemble — baseado em rankings (Mixed)](#🧠 ensemble — baseado em rankings (mixed))** — 1 método(s)
- **[🧠 Ensemble — baseado em modelos (BestSum)](#🧠 ensemble — baseado em modelos (bestsum))** — 1 método(s)
- **[🔗 Híbridos](#🔗 híbridos)** — 2 método(s)
- **[🌱 Embedded](#🌱 embedded)** — 1 método(s)
- **[🎁 Wrappers](#🎁 wrappers)** — 8 método(s)

### 🔹 Filtros univariados

#### `VDM` — Value Difference Metric  ·  ⚪ componente de apoio

Métrica de diferença de valores categóricos condicionada às classes.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Sai:** score global ❌ · ranking ❌ · subconjunto ❌ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `VDM(weighted).run(X, y) -> matriz de distância`
- **Atenção:** não seleciona features; apoia métodos baseados em distância.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`SUPPORT_ONLY`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `anova` — ANOVA F-test  ·  🟢 OK

Estatística F de ANOVA por feature.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Parâmetros:** `k` (nº de features a manter (cutting rule 'K best')) · `cutting_rule` (select_k_best|select_best_percentage|...) · `cutting_param` (parâmetro da cutting rule (k, percent, value))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `anova(X, y)  |  UnivariateFilter('anova', ('K best', k))`
- **Atenção:** Presente na ITMO_FS 0.3.3 (não consta nos docs 0.3.2).

```python
m = fs.get('anova', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `chi2_measure` — Chi-squared  ·  🟢 OK

Estatística qui-quadrado entre feature e classe.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **não negativos** (X≥0); escala recomendada: `minmax`
- **Parâmetros:** `k` (nº de features a manter (cutting rule 'K best')) · `cutting_rule` (select_k_best|select_best_percentage|...) · `cutting_param` (parâmetro da cutting rule (k, percent, value))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `chi2_measure(X, y)  |  UnivariateFilter('chi2_measure', ('K best', k))`

```python
m = fs.get('chi2_measure', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `f_ratio_measure` — F-ratio (Fisher score)  ·  🟢 OK

Calcula o Fisher score de cada feature (separação entre classes).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Parâmetros:** `k` (nº de features a manter (cutting rule 'K best')) · `cutting_rule` (select_k_best|select_best_percentage|...) · `cutting_param` (parâmetro da cutting rule (k, percent, value))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `f_ratio_measure(X, y)  |  UnivariateFilter('f_ratio_measure', ('K best', k))`

```python
m = fs.get('f_ratio_measure', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `fechner_corr` — Fechner correlation  ·  🟢 OK

Correlação de sinal (Fechner) de cada feature.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Parâmetros:** `k` (nº de features a manter (cutting rule 'K best')) · `cutting_rule` (select_k_best|select_best_percentage|...) · `cutting_param` (parâmetro da cutting rule (k, percent, value))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `fechner_corr(X, y)  |  UnivariateFilter('fechner_corr', ('K best', k))`
- **Atenção:** correlação com sinal: 'K best' usa score BRUTO — associações fortemente negativas podem ser ignoradas; considere magnitude.

```python
m = fs.get('fechner_corr', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `fit_criterion_measure` — Fit Criterion  ·  🔴 indisponível (bug 0.3.3)

Critério de ajuste por classe (centros/variâncias).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `fit_criterion_measure(X, y)`
- **Atenção:** bug: np.empty(np.unique(y)) -> TypeError em qualquer entrada.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `gini_index` — Gini index  ·  🟢 OK

Índice de Gini: medida de dispersão estatística por feature.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Parâmetros:** `k` (nº de features a manter (cutting rule 'K best')) · `cutting_rule` (select_k_best|select_best_percentage|...) · `cutting_param` (parâmetro da cutting rule (k, percent, value))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `gini_index(X, y)  |  UnivariateFilter('gini_index', ('K best', k))`

```python
m = fs.get('gini_index', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `information_gain` — Information gain  ·  🟢 OK

Informação mútua I(X;Y)=H(X)-H(X|Y) por feature.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `k` (nº de features a manter (cutting rule 'K best')) · `cutting_rule` (select_k_best|select_best_percentage|...) · `cutting_param` (parâmetro da cutting rule (k, percent, value))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `information_gain(X, y)  |  UnivariateFilter('information_gain', ('K best', k))`

```python
m = fs.get('information_gain', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `kendall_corr` — Kendall correlation  ·  🟢 OK

Correlação de sinal (Kendall) de cada feature.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Parâmetros:** `k` (nº de features a manter (cutting rule 'K best')) · `cutting_rule` (select_k_best|select_best_percentage|...) · `cutting_param` (parâmetro da cutting rule (k, percent, value))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `kendall_corr(X, y)  |  UnivariateFilter('kendall_corr', ('K best', k))`
- **Atenção:** correlação com sinal: 'K best' usa score BRUTO — associações fortemente negativas podem ser ignoradas; considere magnitude.

```python
m = fs.get('kendall_corr', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `laplacian_score` — Laplacian score  ·  🟢 OK

Score laplaciano (não supervisionado); menor é melhor.

- **Entra:** X ✅ · `y`: **não usado** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `k` (nº de features a manter (cutting rule 'K best')) · `cutting_rule` (select_k_best|select_best_percentage|...) · `cutting_param` (parâmetro da cutting rule (k, percent, value))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `laplacian_score(X, y)  |  UnivariateFilter('laplacian_score', ('K best', k))`
- **Atenção:** Presente na ITMO_FS 0.3.3 (não consta nos docs 0.3.2); não supervisionado (menor é melhor).

```python
m = fs.get('laplacian_score', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `pearson_corr` — Pearson correlation  ·  🟢 OK

Correlação de Pearson de cada feature com o alvo.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Parâmetros:** `k` (nº de features a manter (cutting rule 'K best')) · `cutting_rule` (select_k_best|select_best_percentage|...) · `cutting_param` (parâmetro da cutting rule (k, percent, value))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `pearson_corr(X, y)  |  UnivariateFilter('pearson_corr', ('K best', k))`
- **Atenção:** correlação com sinal: 'K best' usa score BRUTO — associações fortemente negativas podem ser ignoradas; considere magnitude.

```python
m = fs.get('pearson_corr', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `qpfs_filter` — QPFS  ·  🟠 dependência ausente

Quadratic Programming Feature Selection.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `qpfs_filter(X, y, r, sigma, solv, fn)`
- **Atenção:** requer solver de QP (quadprog) ausente. Medida univariada (distinta do wrapper qpfs_wrapper).
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`DEPENDENCY_MISSING`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `reliefF_measure` — ReliefF  ·  🟢 OK

Medida ReliefF baseada em vizinhos mais próximos.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `k` (nº de features a manter (cutting rule 'K best')) · `cutting_rule` (select_k_best|select_best_percentage|...) · `cutting_param` (parâmetro da cutting rule (k, percent, value))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `reliefF_measure(X, y)  |  UnivariateFilter('reliefF_measure', ('K best', k))`

```python
m = fs.get('reliefF_measure', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `spearman_corr` — Spearman correlation  ·  🟢 OK

Correlação de Spearman de cada feature com o alvo.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Parâmetros:** `k` (nº de features a manter (cutting rule 'K best')) · `cutting_rule` (select_k_best|select_best_percentage|...) · `cutting_param` (parâmetro da cutting rule (k, percent, value))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `spearman_corr(X, y)  |  UnivariateFilter('spearman_corr', ('K best', k))`
- **Atenção:** correlação com sinal: 'K best' usa score BRUTO — associações fortemente negativas podem ser ignoradas; considere magnitude.

```python
m = fs.get('spearman_corr', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `su_measure` — Symmetric Uncertainty  ·  🟢 OK

Correlação informacional SU(X,Y)=2*I(X;Y)/(H(X)+H(Y)).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `k` (nº de features a manter (cutting rule 'K best')) · `cutting_rule` (select_k_best|select_best_percentage|...) · `cutting_param` (parâmetro da cutting rule (k, percent, value))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `su_measure(X, y)  |  UnivariateFilter('su_measure', ('K best', k))`

```python
m = fs.get('su_measure', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

---

### 🔸 Filtros multivariados

#### `CFR` — CFR  ·  🟢 OK

Maximiza correlação e minimiza redundância.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `n_features` (nº de features a selecionar (processo sequencial))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('CFR', n_features)`
- **Atenção:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('CFR', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `CIFE` — CIFE  ·  🟢 OK

Conditional Infomax Feature Extraction.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `n_features` (nº de features a selecionar (processo sequencial))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('CIFE', n_features)`
- **Atenção:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('CIFE', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `CMIM` — CMIM  ·  🟢 OK

Conditional Mutual Info Maximisation.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `n_features` (nº de features a selecionar (processo sequencial))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('CMIM', n_features)`
- **Atenção:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('CMIM', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `DCSF` — DCSF  ·  🟢 OK

Dynamic change of selected feature.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `n_features` (nº de features a selecionar (processo sequencial))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('DCSF', n_features)`
- **Atenção:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('DCSF', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `DISRWithMassive` — DISR with Massive  ·  🟢 OK

Double Input Symmetric Relevance (kASSI); maximiza info mútua evitando densidade multivariada grande.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `expected_size` (nº de features esperado)
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `DISRWithMassive(expected_size).fit(X,y).transform(X)`

```python
m = fs.get('DISRWithMassive').fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `FCBFDiscreteFilter` — FCBF (discrete)  ·  🟢 OK

Fast Correlation Based Filter para dados discretos (info mútua; remove redundância).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `FCBFDiscreteFilter().fit(X,y).transform(X)`
- **Atenção:** define automaticamente o nº de features (limiar de correlação).

```python
m = fs.get('FCBFDiscreteFilter').fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `ICAP` — ICAP  ·  🟢 OK

Interaction Capping.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `n_features` (nº de features a selecionar (processo sequencial))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('ICAP', n_features)`
- **Atenção:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('ICAP', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `IWFS` — IWFS  ·  🟢 OK

Interaction Weight based feature scoring.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `n_features` (nº de features a selecionar (processo sequencial))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('IWFS', n_features)`
- **Atenção:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('IWFS', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `JMI` — Joint Mutual Information  ·  🟢 OK

Informação mútua conjunta (complementaridade).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `n_features` (nº de features a selecionar (processo sequencial))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('JMI', n_features)`
- **Atenção:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('JMI', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `MIFS` — MIFS  ·  🟢 OK

Relevância menos penalização de redundância (parâmetro beta).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `n_features` (nº de features a selecionar (processo sequencial)) · `beta` (peso de redundância)
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('MIFS', n_features)`
- **Atenção:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('MIFS', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `MIM` — Mutual Information Maximization  ·  🟢 OK

Maximiza relevância (informação mútua) com o alvo.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `n_features` (nº de features a selecionar (processo sequencial))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('MIM', n_features)`
- **Atenção:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('MIM', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `MIMAGA` — MIMAGA  ·  🔴 indisponível (bug 0.3.3)

MIM + algoritmo genético (estocástico, custoso).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MIMAGA(mim_size, pop_size, max_iter, f_target, k1..k4)`
- **Atenção:** requer muitos hiperparâmetros e é estocástico; não incluído por padrão.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `MRI` — MRI  ·  🟢 OK

Max-Relevance and Max-Independence.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `n_features` (nº de features a selecionar (processo sequencial))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('MRI', n_features)`
- **Atenção:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('MRI', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `MRMR` — mRMR  ·  🟢 OK

Máxima relevância e mínima redundância.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `n_features` (nº de features a selecionar (processo sequencial))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('MRMR', n_features)`
- **Atenção:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('MRMR', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `STIR` — STIR  ·  🟢 OK

Seleção via algoritmo STIR (baseado em vizinhança).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `n_features` (nº de features a manter)
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `STIR(n_features_to_keep).fit(X,y).transform(X)`

```python
m = fs.get('STIR', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `TraceRatioFisher` — Trace Ratio (Fisher)  ·  🟢 OK

Trace Ratio supervisionado (versão Fisher, baseado em similaridade).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `n_features` (nº de features)
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `TraceRatioFisher(n_selected).fit(X,y).transform(X)`

```python
m = fs.get('TraceRatioFisher', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `generalizedCriteria` — Generalized Criteria  ·  🟢 OK

Combinação linear de relevância/redundância/dependência (beta, gamma).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: dados **discretizados**; escala recomendada: `discretize`
- **Parâmetros:** `n_features` (nº de features a selecionar (processo sequencial)) · `beta` (peso de redundância) · `gamma` (peso de dependência condicional)
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('generalizedCriteria', n_features)`
- **Atenção:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('generalizedCriteria', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

---

### 🌐 Filtros esparsos

#### `MCFS` — MCFS  ·  🟢 OK (adaptador)

Unsupervised FS for Multi-Cluster Data.

- **Entra:** X ✅ · `y`: **não usado** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `n_features` (nº de features (top do ranking)) · `mode` (unsupervised | label_aware)
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MCFS(...).run(X[, y]); feature_ranking(W)`
- **Atenção:** scheme='dot' é bugado; usamos '0-1'.

```python
m = fs.get('MCFS', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `NDFS` — NDFS  ·  🟢 OK (adaptador)

Nonnegative Discriminative Feature Selection.

- **Entra:** X ✅ · `y`: **não usado** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `n_features` (nº de features (top do ranking)) · `mode` (unsupervised | label_aware)
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `NDFS(...).run(X[, y]); feature_ranking(W)`

```python
m = fs.get('NDFS', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `RFS` — RFS  ·  🟢 OK (adaptador)

Robust Feature Selection (L2,1-norms).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `n_features` (nº de features (top do ranking)) · `mode` (unsupervised | label_aware)
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `RFS(...).run(X[, y]); feature_ranking(W)`

```python
m = fs.get('RFS', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `SPEC` — SPEC  ·  🟢 OK (adaptador)

Spectral Feature Selection.

- **Entra:** X ✅ · `y`: **opcional** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `n_features` (nº de features (top do ranking)) · `mode` (unsupervised | label_aware)
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `SPEC(...).run(X[, y]); feature_ranking(W)`
- **Atenção:** modo não supervisionado (y=None) é bugado; use label_aware.

```python
m = fs.get('SPEC', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `UDFS` — UDFS  ·  🟢 OK (adaptador)

Unsupervised Discriminative Feature Selection.

- **Entra:** X ✅ · `y`: **não usado** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `n_features` (nº de features (top do ranking)) · `mode` (unsupervised | label_aware)
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `UDFS(...).run(X[, y]); feature_ranking(W)`

```python
m = fs.get('UDFS', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

---

### 🧩 Filtros não supervisionados

#### `TraceRatioLaplacian` — Trace Ratio (Laplacian)  ·  🟢 OK (adaptador)

Trace Ratio não supervisionado (Laplacian).

- **Entra:** X ✅ · `y`: **opcional** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `n_features` (nº de features (top do ranking)) · `mode` (unsupervised | label_aware)
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `TraceRatioLaplacian(...).run(X[, y]); feature_ranking(W)`
- **Atenção:** run() retorna (indices, score, lambda).

```python
m = fs.get('TraceRatioLaplacian', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

---

### 🧠 Ensemble — baseado em medidas (WeightBased)

#### `WeightBased` — WeightBased  ·  🟢 OK

Ensemble por fusão de SCORES normalizados de filtros base.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Parâmetros:** `base_measures` (lista de medidas (strings do UnivariateFilter)) · `k` (nº de features (cutting rule)) · `cutting_rule` (regra de corte) · `weights` (pesos por filtro (None=uniforme))
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `WeightBased(filters).fit(X,y); transform(X, cutting_rule[, fusion, weights])`
- **Atenção:** normalização min-max por base pode apagar correlação negativa (harmonize a direção).

```python
m = fs.get('WeightBased', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

---

### 🧠 Ensemble — baseado em rankings (Mixed)

#### `Mixed` — Mixed  ·  🟢 OK

Ensemble por fusão de RANKINGS (robusto à escala).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Parâmetros:** `base_measures` (lista de FUNÇÕES de medida) · `k` (nº de features)
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `Mixed(filter_functions).fit(X,y); transform(X, k[, fusion])`
- **Atenção:** bases são funções de medida (não objetos filtro).

```python
m = fs.get('Mixed', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

---

### 🧠 Ensemble — baseado em modelos (BestSum)

#### `BestSum` — BestSum  ·  🟢 OK (adaptador)

Ensemble model-based: importâncias ponderadas por desempenho de CV (só treino).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `base_measures` (medidas base (via adaptador com selected_features+best_score)) · `k` (nº de features) · `k_each` (nº de features por modelo base)
- **Sai:** score por feature ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `BestSum(models, cutting_rule).fit(X,y); cut()`
- **Atenção:** BestSum marcado 'not stable'; predict() é bugado — usamos fit()+cut().

```python
m = fs.get('BestSum', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

---

### 🔗 Híbridos

#### `FilterWrapperHybrid` — Filter+Wrapper Hybrid  ·  🔴 indisponível (bug 0.3.3)

Filtro rápido seguido de wrapper.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `FilterWrapperHybrid(filter_, wrapper).fit(X,y)`
- **Atenção:** usa RecursiveElimination internamente (bug list.remove em ndarray).
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `Melif` — Melif  ·  🟢 OK

Otimiza pesos de um ensemble de filtros para maximizar um scorer (só treino).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `base_measures` (medidas do ensemble base) · `k` (nº de features) · `estimator` (classificador (default LogisticRegression)) · `scorer` (função scorer(y_true,y_pred) (default f1_macro))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `Melif(filter_ensemble, scorer).fit(X,y,estimator,cutting_rule)`
- **Atenção:** scorer é obrigatório (default fornecido pelo itmofs-lab).

```python
m = fs.get('Melif', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

---

### 🌱 Embedded

#### `MOS` — MOS / MOSS / MOSNS  ·  🟢 OK

Minimizing Overlapping Selection (com/sem SMOTE) via modelo linear regularizado.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `(interno)` (usa loss='hinge' (loss='log' foi removido no sklearn atual))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MOS(model, loss, seed).fit(X,y).transform(X)`
- **Atenção:** loss='log' quebrado no sklearn atual; itmofs-lab usa 'hinge'.

```python
m = fs.get('MOS').fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

---

### 🎁 Wrappers

#### `AddDelWrapper` — Add-Del Wrapper  ·  🔴 indisponível (bug 0.3.3)

Wrapper baseado em busca guiada por classificador.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `AddDelWrapper(estimator, score, maximize, seed).fit(X,y)`
- **Atenção:** bug: score chamado como int -> TypeError.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `BackwardSelection` — Backward Selection  ·  🟢 OK

Remove uma feature por vez até atingir n_features.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `estimator` (classificador sklearn (default LogisticRegression)) · `n_features` (nº de features finais) · `measure` (score(y_true,y_pred) (default accuracy))
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `BackwardSelection(estimator, n_features, measure).fit(X,y)`

```python
m = fs.get('BackwardSelection', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `HillClimbingWrapper` — Hill Climbing  ·  🔴 indisponível (bug 0.3.3)

Wrapper baseado em busca guiada por classificador.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `HillClimbingWrapper(estimator, scorer).fit(X,y)`
- **Atenção:** bug: compara dict com int -> TypeError.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `RecursiveElimination` — Recursive Elimination  ·  🔴 indisponível (bug 0.3.3)

Wrapper baseado em busca guiada por classificador.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `RecursiveElimination(estimator, n_features).fit(X,y)`
- **Atenção:** bug: list.remove em ndarray -> AttributeError.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `SequentialForwardSelection` — Sequential Forward Selection  ·  🟢 OK

Adiciona sequencialmente a feature que mais melhora o classificador.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: escala recomendada: `standard`
- **Parâmetros:** `estimator` (classificador sklearn) · `n_features` (nº de features) · `measure` (score)
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `SequentialForwardSelection(estimator, n_features, measure).fit(X,y)`

```python
m = fs.get('SequentialForwardSelection', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); m.selected_names_
```

#### `SimulatedAnnealing` — Simulated Annealing  ·  🔴 vazamento por design

Wrapper baseado em busca guiada por classificador.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `SimulatedAnnealing(classifier, score, ...).fit(X,y,test_x,test_y)`
- **Atenção:** fit exige dados de teste (leakage por design).
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`LEAKAGE_BY_DESIGN`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `TPhMGWO` — Two-Phase Mutation GWO  ·  🔴 indisponível (bug 0.3.3)

Wrapper baseado em busca guiada por classificador.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `TPhMGWO(...).run(X,y)`
- **Atenção:** usa np.float (removido no numpy>=1.24) -> AttributeError.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `qpfs_wrapper` — QPFS (wrapper)  ·  🟠 dependência ausente

Quadratic Programming Feature Selection na forma de wrapper.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-processamento: nenhum obrigatório
- **Sai:** score global ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `qpfs_wrapper(X, y, alpha, r=None, sigma=None, solv='quadprog', fn=pearson_corr)`
- **Atenção:** requer solver de QP (quadprog) ausente (SolverNotFound). Distinto de qpfs_filter (medida univariada).
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`DEPENDENCY_MISSING`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

---

## 🧪 Compatibilidade e honestidade

Alguns métodos presentes na API da ITMO_FS 0.3.3 **não executam** nesta versão
(bugs da biblioteca, dependência ausente, ou design que exige o teste no
ajuste). Eles permanecem **catalogados e documentados**, e ao serem chamados
levantam `NotSupportedError` com o motivo — nada é mascarado.

| Situação | Exemplos |
|---|---|
| 🔴 Bug na biblioteca 0.3.3 | `fit_criterion_measure`, `RecursiveElimination`, `TPhMGWO`, `HillClimbingWrapper`, `AddDelWrapper`, `FilterWrapperHybrid` |
| 🟠 Dependência ausente | `qpfs_filter` (requer solver de QP) |
| 🔴 Vazamento por design | `SimulatedAnnealing` (exige teste no `fit`) |

O status de cada método aparece em `itmofs-lab list` e nas seções acima.

## 🔬 Sobre o projeto

O `itmofs-lab` nasceu de um **estudo prático, sistemático e reprodutível** da
biblioteca ITMO_FS, no contexto de pesquisa de pós-graduação sobre **Ensemble
Feature Selection**. Cada método foi inspecionado em tempo de execução
(assinatura real, atributos após `fit`, requisitos de dados) e exercitado em
datasets didáticos, respeitando a regra anti-leakage. O resultado é uma camada
fina, uniforme e documentada sobre a ITMO_FS, que preserva o comportamento
nativo da biblioteca e apenas padroniza o uso — sem inventar scores, sem
mascarar erros e sem alterar o pacote original.

## 📖 Documentação em site

Além deste README, há um site navegável (MkDocs Material):

```bash
pip install mkdocs mkdocs-material
mkdocs serve      # http://127.0.0.1:8000
```

## 📌 Como citar

```bibtex
@software{santos_itmofs_lab,
  author  = {Santos, Vinicius de Souza},
  title   = {itmofs-lab: interface uniforme e documentada para selecao de caracteristicas com a ITMO_FS},
  year    = {2026},
  url     = {https://github.com/ViniciusKanh/itmofs-lab}
}
```

## 👤 Autor

**Vinicius de Souza Santos**
Aluno de pós-graduação — Universidade Estadual Paulista (UNESP), Rio Claro
✉️ vinicius-souza.santos@unesp.br

## 📝 Licença

Distribuído sob a licença **MIT** (veja [`LICENSE`](LICENSE)). Este pacote é uma
camada de conveniência sobre a [ITMO_FS](https://github.com/ctlab/ITMO_FS), que
possui autores e licença próprios; o `itmofs-lab` não redistribui nem modifica o
código da ITMO_FS.
