# Laplacian score  (`laplacian_score`)

**Família:** `filters.univariate` — **tipo:** `score_function`  
**Status na ITMO_FS 0.3.3:** `OK` — Executa normalmente.

Score laplaciano (não supervisionado); menor é melhor.

## O que entra

- **X:** sim
- **y (rótulos):** não usado
- **Pré-processamento:** escala recomendada: `standard`

| parâmetro | descrição |
|---|---|
| `k` | nº de features a manter (cutting rule 'K best') |
| `cutting_rule` | select_k_best|select_best_percentage|... |
| `cutting_param` | parâmetro da cutting rule (k, percent, value) |

## O que sai

- score por feature ✅
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`, `scores_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
laplacian_score(X, y)  |  UnivariateFilter('laplacian_score', ('K best', k))
```

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('laplacian_score', k=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info laplacian_score
itmofs-lab run laplacian_score --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.filters.univariate`
