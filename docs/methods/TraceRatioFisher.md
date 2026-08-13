# Trace Ratio (Fisher)  (`TraceRatioFisher`)

**Família:** `filters.multivariate` — **tipo:** `standalone_selector`  
**Status na ITMO_FS 0.3.3:** `OK` — Executa normalmente.

Trace Ratio supervisionado (versão Fisher, baseado em similaridade).

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** escala recomendada: `standard`

| parâmetro | descrição |
|---|---|
| `n_features` | nº de features |

## O que sai

- score por feature ✅
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`, `scores_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
TraceRatioFisher(n_selected).fit(X,y).transform(X)
```

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('TraceRatioFisher', n_features=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info TraceRatioFisher
itmofs-lab run TraceRatioFisher --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.filters.multivariate`
