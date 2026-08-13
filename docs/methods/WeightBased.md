# WeightBased  (`WeightBased`)

**Família:** `ensembles.measure_based` — **tipo:** `ensemble_selector`  
**Status na ITMO_FS 0.3.3:** `OK` — Executa normalmente.

Ensemble por fusão de SCORES normalizados de filtros base.

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** nenhum obrigatório

| parâmetro | descrição |
|---|---|
| `base_measures` | lista de medidas (strings do UnivariateFilter) |
| `k` | nº de features (cutting rule) |
| `cutting_rule` | regra de corte |
| `weights` | pesos por filtro (None=uniforme) |

## O que sai

- score por feature ✅
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`, `scores_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
WeightBased(filters).fit(X,y); transform(X, cutting_rule[, fusion, weights])
```

## Atenções

normalização min-max por base pode apagar correlação negativa (harmonize a direção).

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('WeightBased', k=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info WeightBased
itmofs-lab run WeightBased --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.ensembles.measure_based`
