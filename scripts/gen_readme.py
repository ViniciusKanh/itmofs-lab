"""Gera um README.md completo e bonito, com a documentação de TODOS os métodos
(entradas e saídas), a partir do catálogo central. Serve para GitHub e PyPI.

Execute: python scripts/gen_readme.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from itmofs_lab.core.registry import ENTRIES, families  # noqa: E402
from itmofs_lab.core.spec import STATUS  # noqa: E402

GH = "https://github.com/ViniciusKanh/itmofs-lab"

FAMILY_TITLE = {
    "filters.univariate": "🔹 Filtros univariados",
    "filters.multivariate": "🔸 Filtros multivariados",
    "filters.sparse": "🌐 Filtros esparsos",
    "filters.unsupervised": "🧩 Filtros não supervisionados",
    "ensembles.measure_based": "🧠 Ensemble — baseado em medidas (WeightBased)",
    "ensembles.ranking_based": "🧠 Ensemble — baseado em rankings (Mixed)",
    "ensembles.model_based": "🧠 Ensemble — baseado em modelos (BestSum)",
    "hybrid": "🔗 Híbridos",
    "embedded": "🌱 Embedded",
    "wrappers": "🎁 Wrappers",
}
FAMILY_ORDER = [
    "filters.univariate", "filters.multivariate", "filters.sparse",
    "filters.unsupervised", "ensembles.measure_based", "ensembles.ranking_based",
    "ensembles.model_based", "hybrid", "embedded", "wrappers",
]
STATUS_BADGE = {
    "OK": "🟢 OK",
    "OK_WITH_ADAPTER": "🟢 OK (adaptador)",
    "BROKEN_IN_0_3_3": "🔴 indisponível (bug 0.3.3)",
    "DEPENDENCY_MISSING": "🟠 dependência ausente",
    "LEAKAGE_BY_DESIGN": "🔴 vazamento por design",
    "SUPPORT_ONLY": "⚪ componente de apoio",
}
Y_MAP = {"required": "obrigatório", "optional": "opcional", "not_used": "não usado"}


def anchor(name: str) -> str:
    return name.lower().replace("_", "-").replace(".", "")


def method_block(e) -> str:
    s = e.spec
    pre = []
    if s.requires_discrete:
        pre.append("dados **discretizados**")
    if s.requires_nonnegative:
        pre.append("dados **não negativos** (X≥0)")
    if s.recommends_scaling not in ("optional", "none"):
        pre.append(f"escala recomendada: `{s.recommends_scaling}`")
    pre_txt = "; ".join(pre) if pre else "nenhum obrigatório"

    outs = []
    outs.append("score por feature ✅" if s.outputs_scores else "score global ❌")
    outs.append("ranking ✅" if s.outputs_ranking else "ranking ❌")
    outs.append("subconjunto ✅" if s.outputs_subset else "subconjunto ❌")
    attrs = "`selected_`, `selected_names_`" + (", `scores_`" if s.outputs_scores else "")

    L = []
    L.append(f"#### `{s.name}` — {s.display}  ·  {STATUS_BADGE.get(s.status, s.status)}")
    L.append("")
    L.append(s.summary)
    L.append("")
    L.append(f"- **Entra:** X {'✅' if s.needs_X else '❌'} · `y`: **{Y_MAP.get(s.y, s.y)}** · pré-processamento: {pre_txt}")
    if s.params:
        params = " · ".join(f"`{k}` ({v})" for k, v in s.params.items())
        L.append(f"- **Parâmetros:** {params}")
    L.append(f"- **Sai:** " + " · ".join(outs) + f" · atributos após `fit`: {attrs}")
    L.append(f"- **Assinatura ITMO_FS:** `{s.itmo_signature}`")
    if s.quirks:
        L.append(f"- **Atenção:** {s.quirks}")
    if s.status not in ("OK", "OK_WITH_ADAPTER"):
        L.append(f"- ⚠️ Catalogado e documentado, mas **não executável** nesta versão "
                 f"(`{s.status}`): ao chamar `fit` levanta `NotSupportedError` com o motivo.")
    # exemplo compacto
    ex_kw = "k=10" if "k" in e.kwargs else ("n_features=10" if "n_features" in e.kwargs else "")
    call = f"fs.get('{s.name}'" + (f", {ex_kw}" if ex_kw else "") + ")"
    if s.status in ("OK", "OK_WITH_ADAPTER"):
        L.append("")
        L.append("```python")
        L.append(f"m = {call}.fit(X_train, y_train)")
        L.append("X_sel = m.transform(X_test); m.selected_names_")
        L.append("```")
    L.append("")
    return "\n".join(L)


HEADER = f"""<h1 align="center">itmofs-lab</h1>

<p align="center">
  <strong>Uma interface simples, uniforme e honesta para seleção de características com a
  <a href="https://github.com/ctlab/ITMO_FS">ITMO_FS</a>.</strong><br>
  Todos os métodos com a mesma API, um comando de ajuda que mostra <em>o que entra e o que sai</em>,
  e a documentação completa de cada método aqui no README.
</p>

<p align="center">
  <a href="https://pypi.org/project/itmofs-lab/"><img alt="PyPI" src="https://img.shields.io/pypi/v/itmofs-lab?color=blue&label=PyPI"></a>
  <img alt="Python" src="https://img.shields.io/pypi/pyversions/itmofs-lab">
  <img alt="License" src="https://img.shields.io/pypi/l/itmofs-lab?color=green">
  <img alt="Downloads" src="https://img.shields.io/pypi/dm/itmofs-lab?color=orange">
  <img alt="Status" src="https://img.shields.io/badge/status-ativo-brightgreen">
</p>

<p align="center">
  <code>pip install itmofs-lab</code>
</p>

---
"""

INTRO = """
## Por que existe

A [ITMO_FS](https://github.com/ctlab/ITMO_FS) reúne dezenas de métodos de
**feature selection** (filtros, ensembles, wrappers), mas com uma API
heterogênea: algumas medidas são funções, outras são classes; umas usam
`fit/transform`, outras `run/feature_ranking`; as regras de corte operam sobre
dicionários; e há bugs e requisitos que só aparecem em tempo de execução.

O **itmofs-lab** entrega tudo isso com uma cara só:

- ✅ **API única** — todo método usa `fit` / `transform` e expõe `selected_`,
  `selected_names_` e `scores_`.
- ✅ **Comando de ajuda** — `itmofs-lab info <método>` (ou `m.info()`) mostra
  exatamente **o que entra e o que sai**.
- ✅ **Um arquivo por método**, importável isoladamente.
- ✅ **Honestidade** — métodos que não executam na versão instalada ficam
  documentados e levantam um erro claro em vez de falhar de forma obscura.
- ✅ **Rigor científico** — pensado para que o conjunto de teste **nunca**
  participe da seleção.

## Instalação

```bash
pip install itmofs-lab
```

> **⚠️ Recomendação de ambiente.** A ITMO_FS 0.3.3 é de ~2021. Para os métodos
> rodarem sem erros de runtime, use dependências compatíveis:
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
X_te_sel = m.transform(X_te)        # aplica as mesmas colunas ao teste

print(m.selected_)                  # índices selecionados
print(m.selected_names_)            # nomes das features
print(m.scores_)                    # scores por feature (ou None)
```

## Comando de ajuda: o que entra e o que sai

```bash
itmofs-lab list                     # todos os métodos + status
itmofs-lab families                 # métodos agrupados por família
itmofs-lab info gini_index          # o que entra e o que sai deste método
itmofs-lab run gini_index --dataset breast_cancer -k 10
itmofs-lab version
```

No Python: `fs.info("gini_index")`, `fs.list_methods(family="ensembles")`,
`fs.get("chi2_measure").info()`.

## Um arquivo por método

```python
from itmofs_lab.filters.univariate.gini_index import GiniIndex
from itmofs_lab.ensembles.WeightBased import WeightBased

m = GiniIndex(k=10)                 # equivalente a fs.get("gini_index", k=10)
print(GiniIndex.info())
```

## Regra científica: anti-leakage

```text
dataset → split treino/teste → preprocessing.fit(treino) → seletor.fit(treino)
        → transform(treino) e transform(teste) → classificador → avaliação no teste
```

O conjunto de **teste nunca** participa da seleção. Chame `fit` apenas com
`X_train` (e `y_train` quando supervisionado), aplique `transform` ao teste
depois, e escolha `k`/threshold **somente** por validação cruzada no treino.
"""


def build():
    fams = families()
    # sumário
    toc = ["## 📚 Documentação completa dos métodos", "",
           "Cobertura de **todas as famílias** da ITMO_FS. Clique para ir à seção:", ""]
    total = 0
    for fam in FAMILY_ORDER:
        if fam not in fams:
            continue
        n = len(fams[fam])
        total += n
        toc.append(f"- **[{FAMILY_TITLE[fam]}](#{anchor(FAMILY_TITLE[fam])})** — {n} método(s)")
    toc.insert(2, f"> **{total} métodos** catalogados e documentados.\n")

    by_name = {e.spec.name: e for e in ENTRIES}
    body = []
    for fam in FAMILY_ORDER:
        if fam not in fams:
            continue
        body.append(f"### {FAMILY_TITLE[fam]}")
        body.append("")
        for name in fams[fam]:
            body.append(method_block(by_name[name]))
        body.append("---")
        body.append("")

    compat = """
## 🧪 Compatibilidade e honestidade

Alguns métodos presentes na API da ITMO_FS 0.3.3 **não executam** nesta versão
(bugs da biblioteca, dependência ausente, ou design que exige o teste no
ajuste). Eles permanecem **catalogados e documentados**, e ao serem chamados
levantam `NotSupportedError` com o motivo — nada é mascarado.

| Situação | Exemplos |
|---|---|
| 🔴 Bug na biblioteca 0.3.3 | `fit_criterion_measure`, `RecursiveElimination`, `TPhMGWO`, `HillClimbingWrapper`, `AddDelWrapper`, `FilterWrapperHybrid` |
| 🟠 Dependência ausente | `qpfs_filter` (requer solver de QP) |
| 🔴 Vazamento por design | `SimulatedAnnealing` (exige teste no `fit`) |

O status de cada método aparece em `itmofs-lab list` e nas seções acima.

## 🔬 Sobre o projeto

O `itmofs-lab` nasceu de um **estudo prático, sistemático e reprodutível** da
biblioteca ITMO_FS, no contexto de pesquisa de pós-graduação sobre **Ensemble
Feature Selection**. Cada método foi inspecionado em tempo de execução
(assinatura real, atributos após `fit`, requisitos de dados) e exercitado em
datasets didáticos, respeitando a regra anti-leakage. O resultado é uma camada
fina, uniforme e documentada sobre a ITMO_FS, que preserva o comportamento
nativo da biblioteca e apenas padroniza o uso — sem inventar scores, sem
mascarar erros e sem alterar o pacote original.

## 📖 Documentação em site

Além deste README, há um site navegável (MkDocs Material):

```bash
pip install mkdocs mkdocs-material
mkdocs serve      # http://127.0.0.1:8000
```

## 📌 Como citar

```bibtex
@software{santos_itmofs_lab,
  author  = {Santos, Vinicius de Souza},
  title   = {itmofs-lab: interface uniforme e documentada para selecao de caracteristicas com a ITMO_FS},
  year    = {2026},
  url     = {""" + GH + """}
}
```

## 👤 Autor

**Vinicius de Souza Santos**
Aluno de pós-graduação — Universidade Estadual Paulista (UNESP), Rio Claro
✉️ vinicius-souza.santos@unesp.br

## 📝 Licença

Distribuído sob a licença **MIT** (veja [`LICENSE`](LICENSE)). Este pacote é uma
camada de conveniência sobre a [ITMO_FS](https://github.com/ctlab/ITMO_FS), que
possui autores e licença próprios; o `itmofs-lab` não redistribui nem modifica o
código da ITMO_FS.
"""

    content = HEADER + INTRO + "\n" + "\n".join(toc) + "\n\n" + "\n".join(body) + compat
    (ROOT / "README.md").write_text(content, encoding="utf-8")
    print(f"README.md gerado: {total} métodos documentados, {len(content)} caracteres.")


if __name__ == "__main__":
    build()
