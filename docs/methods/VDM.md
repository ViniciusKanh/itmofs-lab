# Value Difference Metric  (`VDM`)

**Família:** `filters.univariate` — **tipo:** `support_metric`  
**Status na ITMO_FS 0.3.3:** `SUPPORT_ONLY` — Componente de apoio; não seleciona features.

Métrica de diferença de valores categóricos condicionada às classes.

## O que entra

- **X:** sim
- **y (rótulos):** obrigatório
- **Pré-processamento:** nenhum obrigatório

| parâmetro | descrição |
|---|---|
| — | — |

## O que sai

- sem score global ❌
- ranking ❌
- subconjunto ❌
- **Atributos após `fit`:** `selected_`, `selected_names_`
- **Transforma treino e teste:** não

## Assinatura na ITMO_FS

```
VDM(weighted).run(X, y) -> matriz de distância
```

## Atenções

não seleciona features; apoia métodos baseados em distância.

> ⚠️ Este método está **catalogado e documentado**, mas o status `SUPPORT_ONLY` indica que não executa nesta versão. Ver 'Atenções'.

## Exemplo

```python
import itmofs_lab as fs
m = fs.get('VDM')
m.fit(X_train, y_train)      # ajusta SÓ no treino
X_sel = m.transform(X_test)
print(m.selected_names_)
```

Ajuda na linha de comando:

```bash
itmofs-lab info VDM
itmofs-lab run VDM --dataset breast_cancer
```

**Referência ITMO_FS:** `ITMO_FS.filters.univariate`
