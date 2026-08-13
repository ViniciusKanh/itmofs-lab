# MOS / MOSS / MOSNS  (`MOS`)

**Família:** `embedded` — **tipo:** `embedded_selector`  
**Status na ITMO_FS 0.3.3:** `OK` — Executa normalmente.

Minimizing Overlapping Selection (com/sem SMOTE) via modelo linear regularizado.

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** escala recomendada: `standard`

| parâmetro | descrição |
|---|---|
| `(interno)` | usa loss='hinge' (loss='log' foi removido no sklearn atual) |

## O que sai

- sem score global ❌
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
MOS(model, loss, seed).fit(X,y).transform(X)
```

## Atenções

loss='log' quebrado no sklearn atual; itmofs-lab usa 'hinge'.

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('MOS')
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info MOS
itmofs-lab run MOS --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.embedded`
