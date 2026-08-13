# MIMAGA  (`MIMAGA`)

**Família:** `filters.multivariate` — **tipo:** `standalone_selector`  
**Status na ITMO_FS 0.3.3:** `BROKEN_IN_0_3_3` — Quebrado na ITMO_FS 0.3.3 (bug da biblioteca ou incompatibilidade).

MIM + algoritmo genético (estocástico, custoso).

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** nenhum obrigatório

| parâmetro | descrição |
|---|---|
| — | — |

## O que sai

- sem score global ❌
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
MIMAGA(mim_size, pop_size, max_iter, f_target, k1..k4)
```

## Atenções

requer muitos hiperparâmetros e é estocástico; não incluído por padrão.

> ⚠️ Este método está **catalogado e documentado**, mas o status `BROKEN_IN_0_3_3` indica que não executa nesta versão. Ver 'Atenções'.

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('MIMAGA')
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info MIMAGA
itmofs-lab run MIMAGA --dataset breast_cancer
```

**Referência ITMO_FS:** `filters.multivariate`
