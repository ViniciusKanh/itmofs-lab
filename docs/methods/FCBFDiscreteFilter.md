# FCBF (discrete)  (`FCBFDiscreteFilter`)

**Família:** `filters.multivariate` — **tipo:** `standalone_selector`  
**Status na ITMO_FS 0.3.3:** `OK` — Executa normalmente.

Fast Correlation Based Filter para dados discretos (info mútua; remove redundância).

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** dados discretizados; escala recomendada: `discretize`

| parâmetro | descrição |
|---|---|
| — | — |

## O que sai

- sem score global ❌
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
FCBFDiscreteFilter().fit(X,y).transform(X)
```

## Atenções

define automaticamente o nº de features (limiar de correlação).

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('FCBFDiscreteFilter')
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info FCBFDiscreteFilter
itmofs-lab run FCBFDiscreteFilter --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.filters.multivariate`
