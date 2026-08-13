# Two-Phase Mutation GWO  (`TPhMGWO`)

**Família:** `wrappers` — **tipo:** `wrapper_selector`  
**Status na ITMO_FS 0.3.3:** `BROKEN_IN_0_3_3` — Quebrado na ITMO_FS 0.3.3 (bug da biblioteca ou incompatibilidade).

Wrapper baseado em busca guiada por classificador.

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
TPhMGWO(...).run(X,y)
```

## Atenções

usa np.float (removido no numpy>=1.24) -> AttributeError.

> ⚠️ Este método está **catalogado e documentado**, mas o status `BROKEN_IN_0_3_3` indica que não executa nesta versão. Ver 'Atenções'.

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('TPhMGWO')
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info TPhMGWO
itmofs-lab run TPhMGWO --dataset breast_cancer
```

**Referência ITMO_FS:** `wrappers`
