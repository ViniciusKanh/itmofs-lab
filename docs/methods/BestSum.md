# BestSum  (`BestSum`)

**Família:** `ensembles.model_based` — **tipo:** `ensemble_selector`  
**Status na ITMO_FS 0.3.3:** `OK_WITH_ADAPTER` — Executa via adaptador do itmofs-lab (API run/feature_ranking ou modelo).

Ensemble model-based: importâncias ponderadas por desempenho de CV (só treino).

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** escala recomendada: `standard`

| parâmetro | descrição |
|---|---|
| `base_measures` | medidas base (via adaptador com selected_features+best_score) |
| `k` | nº de features |
| `k_each` | nº de features por modelo base |

## O que sai

- score por feature ✅
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`, `scores_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
BestSum(models, cutting_rule).fit(X,y); cut()
```

## Atenções

BestSum marcado 'not stable'; predict() é bugado — usamos fit()+cut().

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('BestSum', k=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info BestSum
itmofs-lab run BestSum --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.ensembles.model_based`
