# itmofs-lab

Wrapper **simples e uniforme** sobre a biblioteca [ITMO_FS](https://github.com/ctlab/ITMO_FS),
para seleção de características (feature selection). Cada método tem a mesma API
(`fit`/`transform`), um comando de ajuda que mostra **o que entra e o que sai**,
e documentação completa.

## Instalação

```bash
pip install itmofs-lab
```

Isso instala também a `ITMO_FS`. Recomenda-se um ambiente com `numpy<2` /
`pandas<2` / `scikit-learn<1.4` (a ITMO_FS 0.3.3 é de ~2021).

## Uso em 30 segundos

```python
import itmofs_lab as fs
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, stratify=y, random_state=42)

m = fs.get("gini_index", k=10)     # escolha o método pelo nome
m.fit(X_tr, y_tr)                  # ajusta SÓ no treino (anti-leakage)
X_tr_sel = m.transform(X_tr)
X_te_sel = m.transform(X_te)       # mesmas colunas no teste

print(m.selected_)                 # índices selecionados
print(m.selected_names_)           # nomes (se passar feature_names no fit)
print(m.scores_)                   # scores por feature (ou None)
```

## Comando de ajuda: o que entra e o que sai

Na linha de comando:

```bash
itmofs-lab list                    # todos os métodos
itmofs-lab info gini_index         # o que entra e o que sai deste método
itmofs-lab run gini_index --dataset breast_cancer -k 10
itmofs-lab families                # métodos por família
```

No Python:

```python
print(fs.info("chi2_measure"))     # texto de ajuda
fs.list_methods(family="ensembles")
m = fs.get("chi2_measure"); print(m.info())
```

## Regra importante (anti-leakage)

O conjunto de **teste nunca** participa da seleção: chame `fit` apenas com
`X_train` (e `y_train` quando supervisionado); aplique `transform` ao teste
depois. Para escolher `k`/threshold, use validação cruzada só no treino.

## Um arquivo por método

Cada método também é importável isoladamente:

```python
from itmofs_lab.filters.univariate.gini_index import GiniIndex
from itmofs_lab.ensembles.WeightBased import WeightBased

m = GiniIndex(k=10)                 # equivalente a fs.get("gini_index", k=10)
print(GiniIndex.info())
```

## Cobertura

Todos os métodos das famílias da ITMO_FS estão **catalogados e documentados**:
filtros (univariados, multivariados, esparsos, não supervisionados), ensembles,
híbridos, embedded e wrappers. Métodos que **não executam** na versão 0.3.3
(bugs da biblioteca, dependência ausente ou design com vazamento) ficam
marcados com o status correspondente e, ao serem chamados, levantam um erro
claro explicando o motivo — nada é mascarado. Veja o [catálogo](catalog.md).
