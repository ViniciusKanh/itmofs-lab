# Backward Selection  (`BackwardSelection`)

**Família:** `wrappers` — **tipo:** `wrapper_selector`  
**Status na ITMO_FS 0.3.3:** `OK` — Executa normalmente.

Remove uma feature por vez até atingir n_features.

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** escala recomendada: `standard`

| parâmetro | descrição |
|---|---|
| `estimator` | classificador sklearn (default LogisticRegression) |
| `n_features` | nº de features finais |
| `measure` | score(y_true,y_pred) (default accuracy) |

## O que sai

- sem score global ❌
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
BackwardSelection(estimator, n_features, measure).fit(X,y)
```

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('BackwardSelection', n_features=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info BackwardSelection
itmofs-lab run BackwardSelection --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.wrappers.deterministic`
