# Melif  (`Melif`)

**Família:** `hybrid` — **tipo:** `hybrid_selector`  
**Status na ITMO_FS 0.3.3:** `OK` — Executa normalmente.

Otimiza pesos de um ensemble de filtros para maximizar um scorer (só treino).

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** escala recomendada: `standard`

| parâmetro | descrição |
|---|---|
| `base_measures` | medidas do ensemble base |
| `k` | nº de features |
| `estimator` | classificador (default LogisticRegression) |
| `scorer` | função scorer(y_true,y_pred) (default f1_macro) |

## O que sai

- sem score global ❌
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
Melif(filter_ensemble, scorer).fit(X,y,estimator,cutting_rule)
```

## Atenções

scorer é obrigatório (default fornecido pelo itmofs-lab).

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('Melif', k=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info Melif
itmofs-lab run Melif --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.hybrid`
