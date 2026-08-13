# SPEC  (`SPEC`)

**Família:** `filters.sparse` — **tipo:** `standalone_selector`  
**Status na ITMO_FS 0.3.3:** `OK_WITH_ADAPTER` — Executa via adaptador do itmofs-lab (API run/feature_ranking ou modelo).

Spectral Feature Selection.

## O que entra

- **X:** sim
- **y (rótulos):** opcional
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
SPEC(...).run(X[, y]); feature_ranking(W)
```

## Atenções

modo não supervisionado (y=None) é bugado; use label_aware.

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('SPEC', n_features=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info SPEC
itmofs-lab run SPEC --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.filters.sparse`
