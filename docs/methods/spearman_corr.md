# Spearman correlation  (`spearman_corr`)

**Família:** `filters.univariate` — **tipo:** `score_function`  
**Status na ITMO_FS 0.3.3:** `OK` — Executa normalmente.

Correlação de Spearman de cada feature com o alvo.

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** nenhum obrigatório

| parâmetro | descrição |
|---|---|
| `k` | nº de features a manter (cutting rule 'K best') |
| `cutting_rule` | select_k_best|select_best_percentage|... |
| `cutting_param` | parâmetro da cutting rule (k, percent, value) |

## O que sai

- score por feature ✅
- ranking ✅
- subconjunto ✅
- **Atributos após `fit`:** `selected_`, `selected_names_`, `scores_`
- **Transforma treino e teste:** sim

## Assinatura na ITMO_FS

```
spearman_corr(X, y)  |  UnivariateFilter('spearman_corr', ('K best', k))
```

## Atenções

correlação com sinal: 'K best' usa score BRUTO — associações fortemente negativas podem ser ignoradas; considere magnitude.

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('spearman_corr', k=10)
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info spearman_corr
itmofs-lab run spearman_corr --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.filters.univariate`
