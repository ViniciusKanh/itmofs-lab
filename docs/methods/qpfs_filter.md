# QPFS  (`qpfs_filter`)

**Família:** `filters.univariate` — **tipo:** `score_function`  
**Status na ITMO_FS 0.3.3:** `DEPENDENCY_MISSING` — Requer dependência externa ausente (ex.: solver de QP).

Quadratic Programming Feature Selection.

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
qpfs_filter(X, y, r, sigma, solv, fn)
```

## Atenções

requer solver de QP (quadprog) ausente.

> ⚠️ Este método está **catalogado e documentado**, mas o status `DEPENDENCY_MISSING` indica que não executa nesta versão. Ver 'Atenções'.

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('qpfs_filter')
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info qpfs_filter
itmofs-lab run qpfs_filter --dataset breast_cancer
```

**Referência ITMO_FS:** `filters.univariate`
