# MRI  (`MRI`)

**Família:** `filters.multivariate` — **tipo:** `criterion_function`  
**Status na ITMO_FS 0.3.3:** `OK` — Executa normalmente.

Max-Relevance and Max-Independence.

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** dados discretizados; escala recomendada: `discretize`

| parâmetro | descrição |
|---|---|
| `n_features` | nº de features a selecionar (processo sequencial) |

## O que sai

- sem score global ❌
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
MultivariateFilter('MRI', n_features)
```

## Atenções

sem score global comparável; ranking = ordem de seleção (score_available=false).

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('MRI', n_features=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info MRI
itmofs-lab run MRI --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.filters.multivariate`
