# Simulated Annealing  (`SimulatedAnnealing`)

**Família:** `wrappers` — **tipo:** `wrapper_selector`  
**Status na ITMO_FS 0.3.3:** `LEAKAGE_BY_DESIGN` — A API exige dados de teste no fit — viola anti-leakage; não recomendado.

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
SimulatedAnnealing(classifier, score, ...).fit(X,y,test_x,test_y)
```

## Atenções

fit exige dados de teste (leakage por design).

> ⚠️ Este método está **catalogado e documentado**, mas o status `LEAKAGE_BY_DESIGN` indica que não executa nesta versão. Ver 'Atenções'.

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('SimulatedAnnealing')
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info SimulatedAnnealing
itmofs-lab run SimulatedAnnealing --dataset breast_cancer
```

**Referência ITMO_FS:** `wrappers`
