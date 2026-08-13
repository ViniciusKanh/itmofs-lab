<h1 align="center">itmofs-lab</h1>

<p align="center">
  <strong>Uma interface simples, uniforme e honesta para seleção de características com a <a href="https://github.com/ctlab/ITMO_FS">ITMO_FS</a>.</strong><br>
  Todos os métodos com a mesma API, um comando de ajuda que mostra <em>o que entra e o que sai</em>, e documentação completa.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/itmofs-lab?label=PyPI">
  <img alt="Status" src="https://img.shields.io/badge/status-ativo-brightgreen">
</p>

---

## Índice

- [Motivação](#motivação)
- [Instalação](#instalação)
- [Uso em 30 segundos](#uso-em-30-segundos)
- [Comando de ajuda: o que entra e o que sai](#comando-de-ajuda-o-que-entra-e-o-que-sai)
- [Um arquivo por método](#um-arquivo-por-método)
- [Catálogo de métodos](#catálogo-de-métodos)
- [Regra científica: anti-leakage](#regra-científica-anti-leakage)
- [Sobre o projeto](#sobre-o-projeto)
- [Compatibilidade](#compatibilidade)
- [Documentação](#documentação)
- [Como citar](#como-citar)
- [Autor](#autor)
- [Licença](#licença)

---

## Motivação

A [ITMO_FS](https://github.com/ctlab/ITMO_FS) é uma biblioteca rica em métodos de
**feature selection** (filtros, ensembles, wrappers), mas sua API é heterogênea:
algumas medidas são funções, outras são classes; umas usam `fit/transform`,
outras `run/feature_ranking`; as regras de corte operam sobre dicionários; e há
particularidades de versão que só aparecem na execução.

O **itmofs-lab** resolve isso oferecendo:

- ✅ **API única** — todo método se usa com `fit` / `transform` e expõe
  `selected_`, `selected_names_` e `scores_`.
- ✅ **Comando de ajuda** (`itmofs-lab info <método>`) que descreve exatamente
  **o que entra** (X, `y`, pré-processamento, parâmetros) e **o que sai**
  (score, ranking, subconjunto).
- ✅ **Um arquivo por método**, importável isoladamente.
- ✅ **Honestidade sobre compatibilidade** — métodos que não executam na versão
  instalada ficam catalogados e documentados, e levantam um erro claro em vez
  de falhar de forma obscura.
- ✅ **Rigor científico** — projetado para que o conjunto de teste **nunca**
  participe da seleção.

## Instalação

```bash
pip install itmofs-lab
```

> **Recomendação de ambiente.** A ITMO_FS 0.3.3 é de ~2021. Para os métodos
> rodarem sem erros de runtime, use versões compatíveis das dependências:
>
> ```bash
> pip install "numpy<2" "pandas<2" "scikit-learn<1.4" itmofs-lab
> ```

## Uso em 30 segundos

```python
import itmofs_lab as fs
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, stratify=y, random_state=42)

m = fs.get("gini_index", k=10)      # escolha o método pelo nome
m.fit(X_tr, y_tr)                   # ajusta SÓ no treino (anti-leakage)
X_tr_sel = m.transform(X_tr)
X_te_sel = m.transform(X_te)        # aplica as mesmas colunas ao teste

print(m.selected_)                  # índices selecionados
print(m.selected_names_)            # nomes (se passar feature_names no fit)
print(m.scores_)                    # scores por feature (ou None)
```

## Comando de ajuda: o que entra e o que sai

Na linha de comando:

```bash
itmofs-lab list                     # todos os métodos + status
itmofs-lab families                 # métodos agrupados por família
itmofs-lab info gini_index          # o que entra e o que sai deste método
itmofs-lab run gini_index --dataset breast_cancer -k 10
itmofs-lab version
```

Exemplo de saída de `itmofs-lab info chi2_measure`:

```
Método: Chi-squared  [chi2_measure]
Família: filters.univariate  |  tipo: score_function
Status na ITMO_FS 0.3.3: OK — Executa normalmente.

ENTRA:
  X: sim
  y: obrigatório
  pré-processamento: dados não negativos (X>=0); escala recomendada: minmax
  parâmetros:
    - k: nº de features a manter (cutting rule 'K best')
    - ...

SAI:
  scores por feature; ranking; subconjunto selecionado; transforma treino e teste
  atributos após fit: selected_, selected_names_, scores_
```

No Python: `fs.info("chi2_measure")`, `fs.list_methods(family="ensembles")`,
`fs.get("chi2_measure").info()`.

## Um arquivo por método

Cada método também é importável isoladamente:

```python
from itmofs_lab.filters.univariate.gini_index import GiniIndex
from itmofs_lab.ensembles.WeightBased import WeightBased

m = GiniIndex(k=10)                 # equivalente a fs.get("gini_index", k=10)
print(GiniIndex.info())
```

## Catálogo de métodos

Cobertura de **todas as famílias** da ITMO_FS:

| Família | Exemplos | Métodos |
|---|---|---:|
| Filtros univariados | `gini_index`, `f_ratio_measure`, `su_measure`, `chi2_measure`, `information_gain`, `reliefF_measure`, correlações | 15 |
| Filtros multivariados | `MRMR`, `JMI`, `CMIM`, `CIFE`, `DCSF`, `MIM`, `FCBFDiscreteFilter`, `STIR`, `TraceRatioFisher` | 17 |
| Filtros esparsos | `MCFS`, `UDFS`, `NDFS`, `RFS`, `SPEC` | 5 |
| Filtros não supervisionados | `TraceRatioLaplacian` | 1 |
| Ensembles | `WeightBased`, `Mixed`, `BestSum` | 3 |
| Híbridos | `Melif`, `FilterWrapperHybrid` | 2 |
| Embedded | `MOS` | 1 |
| Wrappers | `BackwardSelection`, `SequentialForwardSelection`, ... | 7 |

Veja o catálogo completo, com **o que entra / o que sai** de cada método, na
pasta [`docs/`](docs/catalog.md).

## Regra científica: anti-leakage

O conjunto de **teste nunca** participa da seleção de características:

```text
dataset → split treino/teste → preprocessing.fit(treino) → seletor.fit(treino)
        → transform(treino) e transform(teste) → classificador → avaliação no teste
```

Portanto: chame `fit` apenas com `X_train` (e `y_train` quando supervisionado);
aplique `transform` ao teste depois; e escolha `k`/threshold **somente** por
validação cruzada dentro do treino. Qualquer uso do teste na seleção é
considerado vazamento de dados (*data leakage*).

## Sobre o projeto

O `itmofs-lab` nasceu de um **estudo prático, sistemático e reprodutível** da
biblioteca ITMO_FS, no contexto de pesquisa de pós-graduação sobre **Ensemble
Feature Selection**. Cada método foi inspecionado em tempo de execução
(assinatura real, atributos após `fit`, requisitos de dados) e exercitado em
datasets didáticos, respeitando a regra anti-leakage. O resultado desse estudo
foi consolidado neste pacote: uma camada fina, uniforme e documentada sobre a
ITMO_FS, que preserva o comportamento nativo da biblioteca e apenas padroniza o
uso — sem inventar scores, sem mascarar erros e sem alterar o pacote original.

## Compatibilidade

Alguns métodos presentes na API da ITMO_FS 0.3.3 **não executam** nesta versão
por bugs da própria biblioteca, dependências externas ausentes ou design que
exigiria o conjunto de teste no ajuste. Esses métodos permanecem **catalogados e
documentados** e, ao serem chamados, levantam `NotSupportedError` com o motivo:

| Situação | Exemplos |
|---|---|
| Bug na biblioteca 0.3.3 | `fit_criterion_measure`, `RecursiveElimination`, `TPhMGWO`, `HillClimbingWrapper` |
| Dependência ausente | `qpfs_filter` (requer solver de QP) |
| Design com vazamento | `SimulatedAnnealing` (exige teste no `fit`) |

Nada é mascarado: o status de cada método é explícito em `itmofs-lab list` e na
documentação.

## Documentação

- **Markdown**: um arquivo por método em [`docs/methods/`](docs/) + índice em
  [`docs/catalog.md`](docs/catalog.md).
- **Site (MkDocs Material)**:

  ```bash
  pip install mkdocs mkdocs-material
  mkdocs serve         # http://127.0.0.1:8000
  ```

## Como citar

```bibtex
@software{santos_itmofs_lab,
  author  = {Santos, Vinicius de Souza},
  title   = {itmofs-lab: uma interface uniforme e documentada para seleção de características com a ITMO_FS},
  year    = {2026},
  url     = {https://github.com/ViniciusKanh/itmofs-lab}
}
```

## Autor

**Vinicius de Souza Santos**
Aluno de pós-graduação — Universidade Estadual Paulista (UNESP), Rio Claro
✉️ vinicius-souza.santos@unesp.br

## Licença

Distribuído sob a licença **MIT**. Veja [`LICENSE`](LICENSE).

Este pacote é uma camada de conveniência sobre a
[ITMO_FS](https://github.com/ctlab/ITMO_FS), que possui sua própria licença e
autores; o `itmofs-lab` não redistribui nem modifica o código da ITMO_FS.
