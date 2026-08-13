# STIR  (`STIR`)

**Família:** `filters.multivariate` — **tipo:** `standalone_selector`  
**Status na ITMO_FS 0.3.3:** `OK` — Executa normalmente.

Seleção via algoritmo STIR (baseado em vizinhança).

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** escala recomendada: `standard`

| parâmetro | descrição |
|---|---|
| `n_features` | nº de features a manter |

## O que sai

- score por feature ✅
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`, `scores_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
STIR(n_features_to_keep).fit(X,y).transform(X)
```

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('STIR', n_features=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info STIR
itmofs-lab run STIR --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.filters.multivariate`
