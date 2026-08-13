# MCFS  (`MCFS`)

**Família:** `filters.sparse` — **tipo:** `standalone_selector`  
**Status na ITMO_FS 0.3.3:** `OK_WITH_ADAPTER` — Executa via adaptador do itmofs-lab (API run/feature_ranking ou modelo).

Unsupervised FS for Multi-Cluster Data.

## O que entra

- **X:** sim
- **y (rótulos):** não usado
- **Pré-processamento:** escala recomendada: `standard`

| parâmetro | descrição |
|---|---|
| `n_features` | nº de features (top do ranking) |
| `mode` | unsupervised | label_aware |

## O que sai

- sem score global ❌
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
MCFS(...).run(X[, y]); feature_ranking(W)
```

## Atenções

scheme='dot' é bugado; usamos '0-1'.

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('MCFS', n_features=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info MCFS
itmofs-lab run MCFS --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.filters.sparse`
