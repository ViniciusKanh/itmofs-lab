# Fit Criterion  (`fit_criterion_measure`)

**Família:** `filters.univariate` — **tipo:** `score_function`  
**Status na ITMO_FS 0.3.3:** `BROKEN_IN_0_3_3` — Quebrado na ITMO_FS 0.3.3 (bug da biblioteca ou incompatibilidade).

Critério de ajuste por classe (centros/variâncias).

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** nenhum obrigatório

| parâmetro | descrição |
|---|---|
| — | — |

## O que sai

- score por feature ✅
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`, `scores_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
fit_criterion_measure(X, y)
```

## Atenções

bug: np.empty(np.unique(y)) -> TypeError em qualquer entrada.

> ⚠️ Este método está **catalogado e documentado**, mas o status `BROKEN_IN_0_3_3` indica que não executa nesta versão. Ver 'Atenções'.

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('fit_criterion_measure')
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info fit_criterion_measure
itmofs-lab run fit_criterion_measure --dataset breast_cancer
```

**Referência ITMO_FS:** `filters.univariate`
