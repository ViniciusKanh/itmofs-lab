# Sequential Forward Selection  (`SequentialForwardSelection`)

**Família:** `wrappers` — **tipo:** `wrapper_selector`  
**Status na ITMO_FS 0.3.3:** `OK` — Executa normalmente.

Adiciona sequencialmente a feature que mais melhora o classificador.

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** escala recomendada: `standard`

| parâmetro | descrição |
|---|---|
| `estimator` | classificador sklearn |
| `n_features` | nº de features |
| `measure` | score |

## O que sai

- sem score global ❌
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
SequentialForwardSelection(estimator, n_features, measure).fit(X,y)
```

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('SequentialForwardSelection', n_features=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info SequentialForwardSelection
itmofs-lab run SequentialForwardSelection --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.wrappers.deterministic`
