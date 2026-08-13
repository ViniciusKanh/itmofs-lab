# Trace Ratio (Laplacian)  (`TraceRatioLaplacian`)

**Família:** `filters.unsupervised` — **tipo:** `standalone_selector`  
**Status na ITMO_FS 0.3.3:** `OK_WITH_ADAPTER` — Executa via adaptador do itmofs-lab (API run/feature_ranking ou modelo).

Trace Ratio não supervisionado (Laplacian).

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
TraceRatioLaplacian(...).run(X[, y]); feature_ranking(W)
```

## Atenções

run() retorna (indices, score, lambda).

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('TraceRatioLaplacian', n_features=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info TraceRatioLaplacian
itmofs-lab run TraceRatioLaplacian --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.filters.unsupervised`
