<h1 align="center">🧬 itmofs-lab</h1>

<p align="center">
  <strong>Seleção de características com a <a href="https://github.com/ctlab/ITMO_FS">ITMO_FS</a>,
  simples de usar e honesta.</strong><br>
  Uma API única para todos os métodos, um comando de ajuda que mostra
  <em>o que entra e o que sai</em>, e a documentação completa aqui no README.
</p>

<p align="center">
  <a href="https://pypi.org/project/itmofs-lab/"><img alt="PyPI" src="https://img.shields.io/pypi/v/itmofs-lab?color=blue&label=PyPI&logo=pypi&logoColor=white"></a>
  <img alt="Python" src="https://img.shields.io/pypi/pyversions/itmofs-lab?logo=python&logoColor=white">
  <img alt="License" src="https://img.shields.io/pypi/l/itmofs-lab?color=green">
  <img alt="Downloads" src="https://img.shields.io/pypi/dm/itmofs-lab?color=orange">
  <a href="https://github.com/ViniciusKanh/itmofs-lab"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-repo-181717?logo=github"></a>
</p>

<p align="center"><code>pip install itmofs-lab</code></p>

---

## 📖 Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Destaques](#destaques)
- [Instalação](#instalação)
- [Início rápido](#início-rápido)
- [Conceitos essenciais](#conceitos-essenciais)
- [Exemplos práticos](#exemplos-práticos)
- [Documentação completa dos métodos](#documentação-completa-dos-métodos)
- [Tabela-resumo de todos os métodos](#tabela-resumo-de-todos-os-métodos)
- [Correspondência com a API ITMO_FS](#correspondência-com-a-api-itmo_fs)
- [Compatibilidade](#compatibilidade)
- [Como citar](#como-citar) · [Autor](#autor) · [Licença](#licença)

## Sobre o projeto

A [**ITMO_FS**](https://github.com/ctlab/ITMO_FS) é uma biblioteca rica em métodos
de *feature selection* — filtros, ensembles e wrappers. Mas usá-la exige lidar com
uma API heterogênea: algumas medidas são funções, outras são classes; umas usam
`fit/transform`, outras `run/feature_ranking`; as regras de corte operam sobre
dicionários; e há bugs e requisitos que só aparecem em tempo de execução.

O **itmofs-lab** é uma camada fina, uniforme e documentada por cima da ITMO_FS.
Ele nasceu de um **estudo prático, sistemático e reprodutível** da biblioteca, no
contexto de pesquisa de pós-graduação sobre **Ensemble Feature Selection**: cada
método foi inspecionado em tempo de execução (assinatura real, atributos após
`fit`, requisitos de dados) e exercitado em datasets didáticos, sempre respeitando
a regra de que o conjunto de teste **nunca** participa da seleção. O resultado é
esta biblioteca — que preserva o comportamento nativo da ITMO_FS e apenas padroniza
o uso, sem inventar scores, sem mascarar erros e sem alterar o pacote original.

## Destaques

- 🎯 **API única** — todo método usa `fit` / `transform` e expõe `selected_`,
  `selected_names_` e `scores_`.
- ❓ **Comando de ajuda** — `itmofs-lab info <método>` (ou `m.info()`) mostra
  exatamente **o que entra e o que sai**.
- 🗂️ **Um arquivo por método** — importável isoladamente.
- 🤝 **Honestidade** — métodos que não executam na versão instalada ficam
  **documentados** e levantam um erro claro em vez de falhar de forma obscura.
- 🔬 **Rigor científico** — pensado para evitar *data leakage*.
- 📚 **Documentação completa** — os **52 métodos** documentados abaixo,
  com entradas e saídas.

## Instalação

```bash
pip install itmofs-lab
```

> **⚠️ Ambiente recomendado.** A ITMO_FS 0.3.3 é de ~2021. Para os métodos rodarem
> sem erros de runtime, use dependências compatíveis:
>
> ```bash
> pip install "numpy<2" "pandas<2" "scikit-learn<1.4" itmofs-lab
> ```

## Início rápido

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

## Conceitos essenciais

**1) Comando de ajuda — o que entra e o que sai**

```bash
itmofs-lab list                     # todos os métodos + status
itmofs-lab families                 # métodos agrupados por família
itmofs-lab info gini_index          # o que entra e o que sai deste método
itmofs-lab run gini_index --dataset breast_cancer -k 10
itmofs-lab version
```

No Python: `fs.info("gini_index")`, `fs.list_methods(family="ensembles")`,
`fs.get("chi2_measure").info()`.

**2) Um arquivo por método**

```python
from itmofs_lab.filters.univariate.gini_index import GiniIndex
from itmofs_lab.ensembles.WeightBased import WeightBased

m = GiniIndex(k=10)                 # equivalente a fs.get("gini_index", k=10)
print(GiniIndex.info())
```

**3) Regra científica: anti-leakage**

```text
dataset → split treino/teste → preprocessing.fit(treino) → seletor.fit(treino)
        → transform(treino) e transform(teste) → classificador → avaliação no teste
```

O conjunto de **teste nunca** participa da seleção. Chame `fit` apenas com
`X_train` (e `y_train` quando supervisionado), aplique `transform` ao teste depois,
e escolha `k`/threshold **somente** por validação cruzada no treino.

## Exemplos práticos

**Filtro univariado com regra de corte por percentual**

```python
m = fs.get("f_ratio_measure", cutting_rule="select_best_percentage", cutting_param=0.3)
m.fit(X_tr, y_tr)
print(len(m.selected_), "features escolhidas")
```

**Filtro multivariado (controla redundância) — precisa de dados discretizados**

```python
from sklearn.preprocessing import KBinsDiscretizer
disc = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy="uniform").fit(X_tr)
Xd_tr, Xd_te = disc.transform(X_tr).astype(int), disc.transform(X_te).astype(int)
m = fs.get("MRMR", n_features=10).fit(Xd_tr, y_tr)
print(m.selected_)          # ordem de seleção (sem score global)
```

**Ensemble comparando filtros (fusão de scores)**

```python
m = fs.get("WeightBased", base_measures=["GiniIndex", "FRatio", "ReliefF"], k=10)
m.fit(X_tr, y_tr)
print(m.selected_names_)
```


## 📚 Documentação completa dos métodos

> **52 métodos** catalogados. Clique para ir à família:

- 🔹 [Filtros univariados](#filtros-univariados) — 15
- 🔸 [Filtros multivariados](#filtros-multivariados) — 17
- 🌐 [Filtros esparsos](#filtros-esparsos) — 5
- 🧩 [Filtros não supervisionados](#filtros-não-supervisionados) — 1
- 🧠 [Ensemble — baseado em medidas (WeightBased)](#ensemble--baseado-em-medidas-weightbased) — 1
- 🧠 [Ensemble — baseado em rankings (Mixed)](#ensemble--baseado-em-rankings-mixed) — 1
- 🧠 [Ensemble — baseado em modelos (BestSum)](#ensemble--baseado-em-modelos-bestsum) — 1
- 🔗 [Híbridos](#híbridos) — 2
- 🌱 [Embedded](#embedded) — 1
- 🎁 [Wrappers](#wrappers) — 8

### Filtros univariados

🔹 *Avaliam cada feature isoladamente em relação ao alvo.*

#### `VDM` — Value Difference Metric  ·  ⚪ componente de apoio

Métrica de diferença de valores categóricos condicionada às classes.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Sai:** score ❌ · ranking ❌ · subconjunto ❌ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `VDM(weighted).run(X, y) -> matriz de distância`
- **Nota:** não seleciona features; apoia métodos baseados em distância.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`SUPPORT_ONLY`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `anova` — ANOVA F-test  ·  🟢 OK

Estatística F de ANOVA por feature.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Parâmetros:** `k` — nº de features a manter (cutting rule 'K best') · `cutting_rule` — select_k_best|select_best_percentage|... · `cutting_param` — parâmetro da cutting rule (k, percent, value)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `anova(X, y)  |  UnivariateFilter('anova', ('K best', k))`
- **Nota:** Presente na ITMO_FS 0.3.3 (não consta nos docs 0.3.2).

```python
m = fs.get('anova', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `chi2_measure` — Chi-squared  ·  🟢 OK

Estatística qui-quadrado entre feature e classe.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **não negativos** (X≥0); escala: `minmax`
- **Parâmetros:** `k` — nº de features a manter (cutting rule 'K best') · `cutting_rule` — select_k_best|select_best_percentage|... · `cutting_param` — parâmetro da cutting rule (k, percent, value)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `chi2_measure(X, y)  |  UnivariateFilter('chi2_measure', ('K best', k))`

```python
m = fs.get('chi2_measure', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `f_ratio_measure` — F-ratio (Fisher score)  ·  🟢 OK

Calcula o Fisher score de cada feature (separação entre classes).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Parâmetros:** `k` — nº de features a manter (cutting rule 'K best') · `cutting_rule` — select_k_best|select_best_percentage|... · `cutting_param` — parâmetro da cutting rule (k, percent, value)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `f_ratio_measure(X, y)  |  UnivariateFilter('f_ratio_measure', ('K best', k))`

```python
m = fs.get('f_ratio_measure', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `fechner_corr` — Fechner correlation  ·  🟢 OK

Correlação de sinal (Fechner) de cada feature.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Parâmetros:** `k` — nº de features a manter (cutting rule 'K best') · `cutting_rule` — select_k_best|select_best_percentage|... · `cutting_param` — parâmetro da cutting rule (k, percent, value)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `fechner_corr(X, y)  |  UnivariateFilter('fechner_corr', ('K best', k))`
- **Nota:** correlação com sinal: 'K best' usa score BRUTO — associações fortemente negativas podem ser ignoradas; considere magnitude.

```python
m = fs.get('fechner_corr', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `fit_criterion_measure` — Fit Criterion  ·  🔴 indisponível (bug 0.3.3)

Critério de ajuste por classe (centros/variâncias).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `fit_criterion_measure(X, y)`
- **Nota:** bug: np.empty(np.unique(y)) -> TypeError em qualquer entrada.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `gini_index` — Gini index  ·  🟢 OK

Índice de Gini: medida de dispersão estatística por feature.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Parâmetros:** `k` — nº de features a manter (cutting rule 'K best') · `cutting_rule` — select_k_best|select_best_percentage|... · `cutting_param` — parâmetro da cutting rule (k, percent, value)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `gini_index(X, y)  |  UnivariateFilter('gini_index', ('K best', k))`

```python
m = fs.get('gini_index', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `information_gain` — Information gain  ·  🟢 OK

Informação mútua I(X;Y)=H(X)-H(X|Y) por feature.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `k` — nº de features a manter (cutting rule 'K best') · `cutting_rule` — select_k_best|select_best_percentage|... · `cutting_param` — parâmetro da cutting rule (k, percent, value)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `information_gain(X, y)  |  UnivariateFilter('information_gain', ('K best', k))`

```python
m = fs.get('information_gain', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `kendall_corr` — Kendall correlation  ·  🟢 OK

Correlação de sinal (Kendall) de cada feature.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Parâmetros:** `k` — nº de features a manter (cutting rule 'K best') · `cutting_rule` — select_k_best|select_best_percentage|... · `cutting_param` — parâmetro da cutting rule (k, percent, value)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `kendall_corr(X, y)  |  UnivariateFilter('kendall_corr', ('K best', k))`
- **Nota:** correlação com sinal: 'K best' usa score BRUTO — associações fortemente negativas podem ser ignoradas; considere magnitude.

```python
m = fs.get('kendall_corr', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `laplacian_score` — Laplacian score  ·  🟢 OK

Score laplaciano (não supervisionado); menor é melhor.

- **Entra:** X ✅ · `y`: **não usado** · pré-proc.: escala: `standard`
- **Parâmetros:** `k` — nº de features a manter (cutting rule 'K best') · `cutting_rule` — select_k_best|select_best_percentage|... · `cutting_param` — parâmetro da cutting rule (k, percent, value)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `laplacian_score(X, y)  |  UnivariateFilter('laplacian_score', ('K best', k))`
- **Nota:** Presente na ITMO_FS 0.3.3 (não consta nos docs 0.3.2); não supervisionado (menor é melhor).

```python
m = fs.get('laplacian_score', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `pearson_corr` — Pearson correlation  ·  🟢 OK

Correlação de Pearson de cada feature com o alvo.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Parâmetros:** `k` — nº de features a manter (cutting rule 'K best') · `cutting_rule` — select_k_best|select_best_percentage|... · `cutting_param` — parâmetro da cutting rule (k, percent, value)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `pearson_corr(X, y)  |  UnivariateFilter('pearson_corr', ('K best', k))`
- **Nota:** correlação com sinal: 'K best' usa score BRUTO — associações fortemente negativas podem ser ignoradas; considere magnitude.

```python
m = fs.get('pearson_corr', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `qpfs_filter` — QPFS  ·  🟠 dependência ausente

Quadratic Programming Feature Selection.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `qpfs_filter(X, y, r, sigma, solv, fn)`
- **Nota:** requer solver de QP (quadprog) ausente. Medida univariada (distinta do wrapper qpfs_wrapper).
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`DEPENDENCY_MISSING`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `reliefF_measure` — ReliefF  ·  🟢 OK

Medida ReliefF baseada em vizinhos mais próximos.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: escala: `standard`
- **Parâmetros:** `k` — nº de features a manter (cutting rule 'K best') · `cutting_rule` — select_k_best|select_best_percentage|... · `cutting_param` — parâmetro da cutting rule (k, percent, value)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `reliefF_measure(X, y)  |  UnivariateFilter('reliefF_measure', ('K best', k))`

```python
m = fs.get('reliefF_measure', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `spearman_corr` — Spearman correlation  ·  🟢 OK

Correlação de Spearman de cada feature com o alvo.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Parâmetros:** `k` — nº de features a manter (cutting rule 'K best') · `cutting_rule` — select_k_best|select_best_percentage|... · `cutting_param` — parâmetro da cutting rule (k, percent, value)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `spearman_corr(X, y)  |  UnivariateFilter('spearman_corr', ('K best', k))`
- **Nota:** correlação com sinal: 'K best' usa score BRUTO — associações fortemente negativas podem ser ignoradas; considere magnitude.

```python
m = fs.get('spearman_corr', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `su_measure` — Symmetric Uncertainty  ·  🟢 OK

Correlação informacional SU(X,Y)=2*I(X;Y)/(H(X)+H(Y)).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `k` — nº de features a manter (cutting rule 'K best') · `cutting_rule` — select_k_best|select_best_percentage|... · `cutting_param` — parâmetro da cutting rule (k, percent, value)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `su_measure(X, y)  |  UnivariateFilter('su_measure', ('K best', k))`

```python
m = fs.get('su_measure', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```


### Filtros multivariados

🔸 *Avaliam cada feature considerando o subconjunto já escolhido (evitam redundância).*

#### `CFR` — CFR  ·  🟢 OK

Maximiza correlação e minimiza redundância.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `n_features` — nº de features a selecionar (processo sequencial)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('CFR', n_features)`
- **Nota:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('CFR', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `CIFE` — CIFE  ·  🟢 OK

Conditional Infomax Feature Extraction.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `n_features` — nº de features a selecionar (processo sequencial)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('CIFE', n_features)`
- **Nota:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('CIFE', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `CMIM` — CMIM  ·  🟢 OK

Conditional Mutual Info Maximisation.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `n_features` — nº de features a selecionar (processo sequencial)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('CMIM', n_features)`
- **Nota:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('CMIM', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `DCSF` — DCSF  ·  🟢 OK

Dynamic change of selected feature.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `n_features` — nº de features a selecionar (processo sequencial)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('DCSF', n_features)`
- **Nota:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('DCSF', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `DISRWithMassive` — DISR with Massive  ·  🟢 OK

Double Input Symmetric Relevance (kASSI); maximiza info mútua evitando densidade multivariada grande.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `expected_size` — nº de features esperado
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `DISRWithMassive(expected_size).fit(X,y).transform(X)`

```python
m = fs.get('DISRWithMassive').fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `FCBFDiscreteFilter` — FCBF (discrete)  ·  🟢 OK

Fast Correlation Based Filter para dados discretos (info mútua; remove redundância).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `FCBFDiscreteFilter().fit(X,y).transform(X)`
- **Nota:** define automaticamente o nº de features (limiar de correlação).

```python
m = fs.get('FCBFDiscreteFilter').fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `ICAP` — ICAP  ·  🟢 OK

Interaction Capping.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `n_features` — nº de features a selecionar (processo sequencial)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('ICAP', n_features)`
- **Nota:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('ICAP', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `IWFS` — IWFS  ·  🟢 OK

Interaction Weight based feature scoring.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `n_features` — nº de features a selecionar (processo sequencial)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('IWFS', n_features)`
- **Nota:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('IWFS', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `JMI` — Joint Mutual Information  ·  🟢 OK

Informação mútua conjunta (complementaridade).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `n_features` — nº de features a selecionar (processo sequencial)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('JMI', n_features)`
- **Nota:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('JMI', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `MIFS` — MIFS  ·  🟢 OK

Relevância menos penalização de redundância (parâmetro beta).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `n_features` — nº de features a selecionar (processo sequencial) · `beta` — peso de redundância
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('MIFS', n_features)`
- **Nota:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('MIFS', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `MIM` — Mutual Information Maximization  ·  🟢 OK

Maximiza relevância (informação mútua) com o alvo.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `n_features` — nº de features a selecionar (processo sequencial)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('MIM', n_features)`
- **Nota:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('MIM', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `MIMAGA` — MIMAGA  ·  🔴 indisponível (bug 0.3.3)

MIM + algoritmo genético (estocástico, custoso).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MIMAGA(mim_size, pop_size, max_iter, f_target, k1..k4)`
- **Nota:** requer muitos hiperparâmetros e é estocástico; não incluído por padrão.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `MRI` — MRI  ·  🟢 OK

Max-Relevance and Max-Independence.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `n_features` — nº de features a selecionar (processo sequencial)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('MRI', n_features)`
- **Nota:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('MRI', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `MRMR` — mRMR  ·  🟢 OK

Máxima relevância e mínima redundância.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `n_features` — nº de features a selecionar (processo sequencial)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('MRMR', n_features)`
- **Nota:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('MRMR', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `STIR` — STIR  ·  🟢 OK

Seleção via algoritmo STIR (baseado em vizinhança).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: escala: `standard`
- **Parâmetros:** `n_features` — nº de features a manter
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `STIR(n_features_to_keep).fit(X,y).transform(X)`

```python
m = fs.get('STIR', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `TraceRatioFisher` — Trace Ratio (Fisher)  ·  🟢 OK

Trace Ratio supervisionado (versão Fisher, baseado em similaridade).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: escala: `standard`
- **Parâmetros:** `n_features` — nº de features
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `TraceRatioFisher(n_selected).fit(X,y).transform(X)`

```python
m = fs.get('TraceRatioFisher', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `generalizedCriteria` — Generalized Criteria  ·  🟢 OK

Combinação linear de relevância/redundância/dependência (beta, gamma).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: dados **discretizados**; escala: `discretize`
- **Parâmetros:** `n_features` — nº de features a selecionar (processo sequencial) · `beta` — peso de redundância · `gamma` — peso de dependência condicional
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MultivariateFilter('generalizedCriteria', n_features)`
- **Nota:** sem score global comparável; ranking = ordem de seleção (score_available=false).

```python
m = fs.get('generalizedCriteria', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```


### Filtros esparsos

🌐 *Métodos espectrais/esparsos baseados em grafos e regularização.*

#### `MCFS` — MCFS  ·  🟢 OK (adaptador)

Unsupervised FS for Multi-Cluster Data.

- **Entra:** X ✅ · `y`: **não usado** · pré-proc.: escala: `standard`
- **Parâmetros:** `n_features` — nº de features (top do ranking) · `mode` — unsupervised | label_aware
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MCFS(...).run(X[, y]); feature_ranking(W)`
- **Nota:** scheme='dot' é bugado; usamos '0-1'.

```python
m = fs.get('MCFS', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `NDFS` — NDFS  ·  🟢 OK (adaptador)

Nonnegative Discriminative Feature Selection.

- **Entra:** X ✅ · `y`: **não usado** · pré-proc.: escala: `standard`
- **Parâmetros:** `n_features` — nº de features (top do ranking) · `mode` — unsupervised | label_aware
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `NDFS(...).run(X[, y]); feature_ranking(W)`

```python
m = fs.get('NDFS', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `RFS` — RFS  ·  🟢 OK (adaptador)

Robust Feature Selection (L2,1-norms).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: escala: `standard`
- **Parâmetros:** `n_features` — nº de features (top do ranking) · `mode` — unsupervised | label_aware
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `RFS(...).run(X[, y]); feature_ranking(W)`

```python
m = fs.get('RFS', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `SPEC` — SPEC  ·  🟢 OK (adaptador)

Spectral Feature Selection.

- **Entra:** X ✅ · `y`: **opcional** · pré-proc.: escala: `standard`
- **Parâmetros:** `n_features` — nº de features (top do ranking) · `mode` — unsupervised | label_aware
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `SPEC(...).run(X[, y]); feature_ranking(W)`
- **Nota:** modo não supervisionado (y=None) é bugado; use label_aware.

```python
m = fs.get('SPEC', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `UDFS` — UDFS  ·  🟢 OK (adaptador)

Unsupervised Discriminative Feature Selection.

- **Entra:** X ✅ · `y`: **não usado** · pré-proc.: escala: `standard`
- **Parâmetros:** `n_features` — nº de features (top do ranking) · `mode` — unsupervised | label_aware
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `UDFS(...).run(X[, y]); feature_ranking(W)`

```python
m = fs.get('UDFS', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```


### Filtros não supervisionados

🧩 *Preservam a estrutura dos dados sem usar rótulos.*

#### `TraceRatioLaplacian` — Trace Ratio (Laplacian)  ·  🟢 OK (adaptador)

Trace Ratio não supervisionado (Laplacian).

- **Entra:** X ✅ · `y`: **opcional** · pré-proc.: escala: `standard`
- **Parâmetros:** `n_features` — nº de features (top do ranking) · `mode` — unsupervised | label_aware
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `TraceRatioLaplacian(...).run(X[, y]); feature_ranking(W)`
- **Nota:** run() retorna (indices, score, lambda).

```python
m = fs.get('TraceRatioLaplacian', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```


### Ensemble — baseado em medidas (WeightBased)

🧠 *Combina os SCORES normalizados de vários filtros.*

#### `WeightBased` — WeightBased  ·  🟢 OK

Ensemble por fusão de SCORES normalizados de filtros base.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Parâmetros:** `base_measures` — lista de medidas (strings do UnivariateFilter) · `k` — nº de features (cutting rule) · `cutting_rule` — regra de corte · `weights` — pesos por filtro (None=uniforme)
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `WeightBased(filters).fit(X,y); transform(X, cutting_rule[, fusion, weights])`
- **Nota:** normalização min-max por base pode apagar correlação negativa (harmonize a direção).

```python
m = fs.get('WeightBased', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```


### Ensemble — baseado em rankings (Mixed)

🧠 *Combina os RANKINGS de vários filtros (robusto à escala).*

#### `Mixed` — Mixed  ·  🟢 OK

Ensemble por fusão de RANKINGS (robusto à escala).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Parâmetros:** `base_measures` — lista de FUNÇÕES de medida · `k` — nº de features
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `Mixed(filter_functions).fit(X,y); transform(X, k[, fusion])`
- **Nota:** bases são funções de medida (não objetos filtro).

```python
m = fs.get('Mixed', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```


### Ensemble — baseado em modelos (BestSum)

🧠 *Pondera importâncias de modelos pelo desempenho em validação cruzada.*

#### `BestSum` — BestSum  ·  🟢 OK (adaptador)

Ensemble model-based: importâncias ponderadas por desempenho de CV (só treino).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: escala: `standard`
- **Parâmetros:** `base_measures` — medidas base (via adaptador com selected_features+best_score) · `k` — nº de features · `k_each` — nº de features por modelo base
- **Sai:** score ✅ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`, `scores_`
- **Assinatura ITMO_FS:** `BestSum(models, cutting_rule).fit(X,y); cut()`
- **Nota:** BestSum marcado 'not stable'; predict() é bugado — usamos fit()+cut().

```python
m = fs.get('BestSum', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```


### Híbridos

🔗 *Combinam mecanismos complementares (filtro + otimização/wrapper).*

#### `FilterWrapperHybrid` — Filter+Wrapper Hybrid  ·  🔴 indisponível (bug 0.3.3)

Filtro rápido seguido de wrapper.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `FilterWrapperHybrid(filter_, wrapper).fit(X,y)`
- **Nota:** usa RecursiveElimination internamente (bug list.remove em ndarray).
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `Melif` — Melif  ·  🟢 OK

Otimiza pesos de um ensemble de filtros para maximizar um scorer (só treino).

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: escala: `standard`
- **Parâmetros:** `base_measures` — medidas do ensemble base · `k` — nº de features · `estimator` — classificador (default LogisticRegression) · `scorer` — função scorer(y_true,y_pred) (default f1_macro)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `Melif(filter_ensemble, scorer).fit(X,y,estimator,cutting_rule)`
- **Nota:** scorer é obrigatório (default fornecido pelo itmofs-lab).

```python
m = fs.get('Melif', k=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```


### Embedded

🌱 *Selecionam durante o ajuste do modelo (coeficientes/regularização).*

#### `MOS` — MOS / MOSS / MOSNS  ·  🟢 OK

Minimizing Overlapping Selection (com/sem SMOTE) via modelo linear regularizado.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: escala: `standard`
- **Parâmetros:** `(interno)` — usa loss='hinge' (loss='log' foi removido no sklearn atual)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `MOS(model, loss, seed).fit(X,y).transform(X)`
- **Nota:** loss='log' quebrado no sklearn atual; itmofs-lab usa 'hinge'.

```python
m = fs.get('MOS').fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```


### Wrappers

🎁 *Buscam subconjuntos guiados pelo desempenho de um classificador.*

#### `AddDelWrapper` — Add-Del Wrapper  ·  🔴 indisponível (bug 0.3.3)

Wrapper baseado em busca guiada por classificador.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `AddDelWrapper(estimator, score, maximize, seed).fit(X,y)`
- **Nota:** bug: score chamado como int -> TypeError.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `BackwardSelection` — Backward Selection  ·  🟢 OK

Remove uma feature por vez até atingir n_features.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: escala: `standard`
- **Parâmetros:** `estimator` — classificador sklearn (default LogisticRegression) · `n_features` — nº de features finais · `measure` — score(y_true,y_pred) (default accuracy)
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `BackwardSelection(estimator, n_features, measure).fit(X,y)`

```python
m = fs.get('BackwardSelection', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `HillClimbingWrapper` — Hill Climbing  ·  🔴 indisponível (bug 0.3.3)

Wrapper baseado em busca guiada por classificador.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `HillClimbingWrapper(estimator, scorer).fit(X,y)`
- **Nota:** bug: compara dict com int -> TypeError.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `RecursiveElimination` — Recursive Elimination  ·  🔴 indisponível (bug 0.3.3)

Wrapper baseado em busca guiada por classificador.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `RecursiveElimination(estimator, n_features).fit(X,y)`
- **Nota:** bug: list.remove em ndarray -> AttributeError.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `SequentialForwardSelection` — Sequential Forward Selection  ·  🟢 OK

Adiciona sequencialmente a feature que mais melhora o classificador.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: escala: `standard`
- **Parâmetros:** `estimator` — classificador sklearn · `n_features` — nº de features · `measure` — score
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `SequentialForwardSelection(estimator, n_features, measure).fit(X,y)`

```python
m = fs.get('SequentialForwardSelection', n_features=10).fit(X_train, y_train)
X_sel = m.transform(X_test); print(m.selected_names_)
```

#### `SimulatedAnnealing` — Simulated Annealing  ·  🔴 vazamento por design

Wrapper baseado em busca guiada por classificador.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `SimulatedAnnealing(classifier, score, ...).fit(X,y,test_x,test_y)`
- **Nota:** fit exige dados de teste (leakage por design).
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`LEAKAGE_BY_DESIGN`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `TPhMGWO` — Two-Phase Mutation GWO  ·  🔴 indisponível (bug 0.3.3)

Wrapper baseado em busca guiada por classificador.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `TPhMGWO(...).run(X,y)`
- **Nota:** usa np.float (removido no numpy>=1.24) -> AttributeError.
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`BROKEN_IN_0_3_3`): ao chamar `fit` levanta `NotSupportedError` com o motivo.

#### `qpfs_wrapper` — QPFS (wrapper)  ·  🟠 dependência ausente

Quadratic Programming Feature Selection na forma de wrapper.

- **Entra:** X ✅ · `y`: **obrigatório** · pré-proc.: nenhum obrigatório
- **Sai:** score ❌ · ranking ✅ · subconjunto ✅ · atributos após `fit`: `selected_`, `selected_names_`
- **Assinatura ITMO_FS:** `qpfs_wrapper(X, y, alpha, r=None, sigma=None, solv='quadprog', fn=pearson_corr)`
- **Nota:** requer solver de QP (quadprog) ausente (SolverNotFound). Distinto de qpfs_filter (medida univariada).
- ⚠️ Catalogado e documentado, mas **não executável** nesta versão (`DEPENDENCY_MISSING`): ao chamar `fit` levanta `NotSupportedError` com o motivo.


## 📋 Tabela-resumo de todos os métodos

Legenda de status: 🟢 executa · 🟢ad via adaptador · 🟠 dependência ausente · 🔴 indisponível na 0.3.3 · ⚪ apoio.

| # | Método | Família | Tipo | Usa `y` | Score | Status |
|---:|---|---|---|:--:|:--:|:--:|
| 1 | `VDM` | filters.univariate | support_metric | sim | — | ⚪ |
| 2 | `anova` | filters.univariate | score_function | sim | ✅ | 🟢 |
| 3 | `chi2_measure` | filters.univariate | score_function | sim | ✅ | 🟢 |
| 4 | `f_ratio_measure` | filters.univariate | score_function | sim | ✅ | 🟢 |
| 5 | `fechner_corr` | filters.univariate | score_function | sim | ✅ | 🟢 |
| 6 | `fit_criterion_measure` | filters.univariate | score_function | sim | ✅ | 🔴 |
| 7 | `gini_index` | filters.univariate | score_function | sim | ✅ | 🟢 |
| 8 | `information_gain` | filters.univariate | score_function | sim | ✅ | 🟢 |
| 9 | `kendall_corr` | filters.univariate | score_function | sim | ✅ | 🟢 |
| 10 | `laplacian_score` | filters.univariate | score_function | não | ✅ | 🟢 |
| 11 | `pearson_corr` | filters.univariate | score_function | sim | ✅ | 🟢 |
| 12 | `qpfs_filter` | filters.univariate | score_function | sim | — | 🟠 |
| 13 | `reliefF_measure` | filters.univariate | score_function | sim | ✅ | 🟢 |
| 14 | `spearman_corr` | filters.univariate | score_function | sim | ✅ | 🟢 |
| 15 | `su_measure` | filters.univariate | score_function | sim | ✅ | 🟢 |
| 16 | `CFR` | filters.multivariate | criterion_function | sim | — | 🟢 |
| 17 | `CIFE` | filters.multivariate | criterion_function | sim | — | 🟢 |
| 18 | `CMIM` | filters.multivariate | criterion_function | sim | — | 🟢 |
| 19 | `DCSF` | filters.multivariate | criterion_function | sim | — | 🟢 |
| 20 | `DISRWithMassive` | filters.multivariate | standalone_selector | sim | — | 🟢 |
| 21 | `FCBFDiscreteFilter` | filters.multivariate | standalone_selector | sim | — | 🟢 |
| 22 | `ICAP` | filters.multivariate | criterion_function | sim | — | 🟢 |
| 23 | `IWFS` | filters.multivariate | criterion_function | sim | — | 🟢 |
| 24 | `JMI` | filters.multivariate | criterion_function | sim | — | 🟢 |
| 25 | `MIFS` | filters.multivariate | criterion_function | sim | — | 🟢 |
| 26 | `MIM` | filters.multivariate | criterion_function | sim | — | 🟢 |
| 27 | `MIMAGA` | filters.multivariate | standalone_selector | sim | — | 🔴 |
| 28 | `MRI` | filters.multivariate | criterion_function | sim | — | 🟢 |
| 29 | `MRMR` | filters.multivariate | criterion_function | sim | — | 🟢 |
| 30 | `STIR` | filters.multivariate | standalone_selector | sim | ✅ | 🟢 |
| 31 | `TraceRatioFisher` | filters.multivariate | standalone_selector | sim | ✅ | 🟢 |
| 32 | `generalizedCriteria` | filters.multivariate | criterion_function | sim | — | 🟢 |
| 33 | `MCFS` | filters.sparse | standalone_selector | não | — | 🟢ad |
| 34 | `NDFS` | filters.sparse | standalone_selector | não | — | 🟢ad |
| 35 | `RFS` | filters.sparse | standalone_selector | sim | — | 🟢ad |
| 36 | `SPEC` | filters.sparse | standalone_selector | opc. | — | 🟢ad |
| 37 | `UDFS` | filters.sparse | standalone_selector | não | — | 🟢ad |
| 38 | `TraceRatioLaplacian` | filters.unsupervised | standalone_selector | opc. | — | 🟢ad |
| 39 | `WeightBased` | ensembles.measure_based | ensemble_selector | sim | ✅ | 🟢 |
| 40 | `Mixed` | ensembles.ranking_based | ensemble_selector | sim | — | 🟢 |
| 41 | `BestSum` | ensembles.model_based | ensemble_selector | sim | ✅ | 🟢ad |
| 42 | `FilterWrapperHybrid` | hybrid | hybrid_selector | sim | — | 🔴 |
| 43 | `Melif` | hybrid | hybrid_selector | sim | — | 🟢 |
| 44 | `MOS` | embedded | embedded_selector | sim | — | 🟢 |
| 45 | `AddDelWrapper` | wrappers | wrapper_selector | sim | — | 🔴 |
| 46 | `BackwardSelection` | wrappers | wrapper_selector | sim | — | 🟢 |
| 47 | `HillClimbingWrapper` | wrappers | wrapper_selector | sim | — | 🔴 |
| 48 | `RecursiveElimination` | wrappers | wrapper_selector | sim | — | 🔴 |
| 49 | `SequentialForwardSelection` | wrappers | wrapper_selector | sim | — | 🟢 |
| 50 | `SimulatedAnnealing` | wrappers | wrapper_selector | sim | — | 🔴 |
| 51 | `TPhMGWO` | wrappers | wrapper_selector | sim | — | 🔴 |
| 52 | `qpfs_wrapper` | wrappers | wrapper_selector | sim | — | 🟠 |

## Correspondência com a API ITMO_FS

Uma reconciliação completa (nos dois sentidos) entre os métodos do `itmofs-lab` e a
API oficial da ITMO_FS — incluindo interfaces internas, regras de corte e
utilitários de apoio — está em
[`docs/CORRESPONDENCIA_API.md`](https://github.com/ViniciusKanh/itmofs-lab/blob/main/docs/CORRESPONDENCIA_API.md).
Resumo: a biblioteca cobre **100%** dos símbolos públicos da API 0.3.2, mais os
extras da 0.3.3 (`anova`, `laplacian_score`).

## Compatibilidade

Alguns métodos presentes na API da ITMO_FS 0.3.3 **não executam** nesta versão
(bugs da biblioteca, dependência ausente, ou design que exige o teste no ajuste).
Eles permanecem **catalogados e documentados**, e ao serem chamados levantam
`NotSupportedError` com o motivo — nada é mascarado.

| Situação | Exemplos |
|---|---|
| 🔴 Bug na biblioteca 0.3.3 | `fit_criterion_measure`, `RecursiveElimination`, `TPhMGWO`, `HillClimbingWrapper`, `AddDelWrapper`, `FilterWrapperHybrid` |
| 🟠 Dependência ausente | `qpfs_filter`, `qpfs_wrapper` (requerem solver de QP) |
| 🔴 Vazamento por design | `SimulatedAnnealing` (exige teste no `fit`) |

## Documentação em site

Além deste README, há um site navegável (MkDocs Material):

```bash
pip install mkdocs mkdocs-material
mkdocs serve      # http://127.0.0.1:8000
```

## Como citar

```bibtex
@software{santos_itmofs_lab,
  author  = {Santos, Vinicius de Souza},
  title   = {itmofs-lab: interface uniforme e documentada para selecao de caracteristicas com a ITMO_FS},
  year    = {2026},
  url     = {https://github.com/ViniciusKanh/itmofs-lab}
}
```

## Autor

**Vinicius de Souza Santos** — Aluno de pós-graduação, Universidade Estadual
Paulista (UNESP), Rio Claro · ✉️ vinicius-souza.santos@unesp.br

## Licença

Distribuído sob a licença **MIT** (veja [`LICENSE`](LICENSE)). Este pacote é uma
camada de conveniência sobre a [ITMO_FS](https://github.com/ctlab/ITMO_FS), que
possui autores e licença próprios; o `itmofs-lab` não redistribui nem modifica o
código da ITMO_FS.
