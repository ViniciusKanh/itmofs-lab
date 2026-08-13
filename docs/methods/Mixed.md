# Mixed  (`Mixed`)

**Família:** `ensembles.ranking_based` — **tipo:** `ensemble_selector`  
**Status na ITMO_FS 0.3.3:** `OK` — Executa normalmente.

Ensemble por fusão de RANKINGS (robusto à escala).

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** nenhum obrigatório

| parâmetro | descrição |
|---|---|
| `base_measures` | lista de FUNÇÕES de medida |
| `k` | nº de features |

## O que sai

- sem score global ❌
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
Mixed(filter_functions).fit(X,y); transform(X, k[, fusion])
```

## Atenções

bases são funções de medida (não objetos filtro).

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('Mixed', k=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info Mixed
itmofs-lab run Mixed --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.ensembles.ranking_based`
