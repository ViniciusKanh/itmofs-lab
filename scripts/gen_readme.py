"""Gera um README.md completo e bonito: introduz o projeto, documenta TODOS os
métodos (entradas/saídas) e termina com uma tabela-resumo. Serve para GitHub e PyPI.

Execute: python scripts/gen_readme.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from itmofs_lab.core.registry import ENTRIES, families  # noqa: E402

GH = "https://github.com/ViniciusKanh/itmofs-lab"

FAMILY_ORDER = [
    "filters.univariate", "filters.multivariate", "filters.sparse",
    "filters.unsupervised", "ensembles.measure_based", "ensembles.ranking_based",
    "ensembles.model_based", "hybrid", "embedded", "wrappers",
]
FAMILY_TITLE = {
    "filters.univariate": "Filtros univariados",
    "filters.multivariate": "Filtros multivariados",
    "filters.sparse": "Filtros esparsos",
    "filters.unsupervised": "Filtros não supervisionados",
    "ensembles.measure_based": "Ensemble — baseado em medidas (WeightBased)",
    "ensembles.ranking_based": "Ensemble — baseado em rankings (Mixed)",
    "ensembles.model_based": "Ensemble — baseado em modelos (BestSum)",
    "hybrid": "Híbridos",
    "embedded": "Embedded",
    "wrappers": "Wrappers",
}
FAMILY_EMOJI = {
    "filters.univariate": "🔹", "filters.multivariate": "🔸", "filters.sparse": "🌐",
    "filters.unsupervised": "🧩", "ensembles.measure_based": "🧠",
    "ensembles.ranking_based": "🧠", "ensembles.model_based": "🧠",
    "hybrid": "🔗", "embedded": "🌱", "wrappers": "🎁",
}
FAMILY_LEAD = {
    "filters.univariate": "Avaliam cada feature isoladamente em relação ao alvo.",
    "filters.multivariate": "Avaliam cada feature considerando o subconjunto já escolhido (evitam redundância).",
    "filters.sparse": "Métodos espectrais/esparsos baseados em grafos e regularização.",
    "filters.unsupervised": "Preservam a estrutura dos dados sem usar rótulos.",
    "ensembles.measure_based": "Combina os SCORES normalizados de vários filtros.",
    "ensembles.ranking_based": "Combina os RANKINGS de vários filtros (robusto à escala).",
    "ensembles.model_based": "Pondera importâncias de modelos pelo desempenho em validação cruzada.",
    "hybrid": "Combinam mecanismos complementares (filtro + otimização/wrapper).",
    "embedded": "Selecionam durante o ajuste do modelo (coeficientes/regularização).",
    "wrappers": "Buscam subconjuntos guiados pelo desempenho de um classificador.",
}
STATUS_BADGE = {
    "OK": "🟢 OK",
    "OK_WITH_ADAPTER": "🟢 OK (adaptador)",
    "BROKEN_IN_0_3_3": "🔴 indisponível (bug 0.3.3)",
    "DEPENDENCY_MISSING": "🟠 dependência ausente",
    "LEAKAGE_BY_DESIGN": "🔴 vazamento por design",
    "SUPPORT_ONLY": "⚪ componente de apoio",
}
STATUS_SHORT = {
    "OK": "🟢", "OK_WITH_ADAPTER": "🟢ad", "BROKEN_IN_0_3_3": "🔴",
    "DEPENDENCY_MISSING": "🟠", "LEAKAGE_BY_DESIGN": "🔴", "SUPPORT_ONLY": "⚪",
}
Y_MAP = {"required": "obrigatório", "optional": "opcional", "not_used": "não usado"}
Y_SHORT = {"required": "sim", "optional": "opc.", "not_used": "não"}


def gh_anchor(text: str) -> str:
    a = text.strip().lower()
    a = re.sub(r"[^\w\s-]", "", a, flags=re.UNICODE)  # remove pontuação/emoji
    a = a.strip().replace(" ", "-")
    return a


def method_block(e) -> str:
    s = e.spec
    pre = []
    if s.requires_discrete:
        pre.append("dados **discretizados**")
    if s.requires_nonnegative:
        pre.append("dados **não negativos** (X≥0)")
    if s.recommends_scaling not in ("optional", "none"):
        pre.append(f"escala: `{s.recommends_scaling}`")
    pre_txt = "; ".join(pre) if pre else "nenhum obrigatório"
    outs = []
    outs.append("score ✅" if s.outputs_scores else "score ❌")
    outs.append("ranking ✅" if s.outputs_ranking else "ranking ❌")
    outs.append("subconjunto ✅" if s.outputs_subset else "subconjunto ❌")
    attrs = "`selected_`, `selected_names_`" + (", `scores_`" if s.outputs_scores else "")

    L = []
    L.append(f"#### `{s.name}` — {s.display}  ·  {STATUS_BADGE.get(s.status, s.status)}")
    L.append("")
    L.append(s.summary)
    L.append("")
    L.append(f"- **Entra:** X {'✅' if s.needs_X else '❌'} · `y`: **{Y_MAP.get(s.y, s.y)}** · pré-proc.: {pre_txt}")
    if s.params:
        L.append("- **Parâmetros:** " + " · ".join(f"`{k}` — {v}" for k, v in s.params.items()))
    L.append(f"- **Sai:** " + " · ".join(outs) + f" · atributos após `fit`: {attrs}")
    L.append(f"- **Assinatura ITMO_FS:** `{s.itmo_signature}`")
    if s.quirks:
        L.append(f"- **Nota:** {s.quirks}")
    if s.status not in ("OK", "OK_WITH_ADAPTER"):
        L.append(f"- ⚠️ Catalogado e documentado, mas **não executável** nesta versão "
                 f"(`{s.status}`): ao chamar `fit` levanta `NotSupportedError` com o motivo.")
    ex_kw = "k=10" if "k" in e.kwargs else ("n_features=10" if "n_features" in e.kwargs else "")
    if s.status in ("OK", "OK_WITH_ADAPTER"):
        call = f"fs.get('{s.name}'" + (f", {ex_kw}" if ex_kw else "") + ")"
        L.append("")
        L.append("```python")
        L.append(f"m = {call}.fit(X_train, y_train)")
        L.append("X_sel = m.transform(X_test); print(m.selected_names_)")
        L.append("```")
    L.append("")
    return "\n".join(L)


HEADER = f"""<h1 align="center">🧬 itmofs-lab</h1>

<p align="center">
  <strong>Seleção de características com a <a href="https://github.com/ctlab/ITMO_FS">ITMO_FS</a>,
  simples de usar e honesta.</strong><br>
  Uma API única para todos os métodos, um comando de ajuda que mostra
  <em>o que entra e o que sai</em>, e a documentação completa aqui no README.
</p>

<p align="center">
  <a href="https://pypi.org/project/itmofs-lab/"><img alt="PyPI" src="https://img.shields.io/pypi/v/itmofs-lab?color=blue&label=PyPI&logo=pypi&logoColor=white"></a>
  <img alt="Python" src="https://img.shields.io/pypi/pyversions/itmofs-lab?logo=python&logoColor=white">
  <img alt="License" src="https://img.shields.io/pypi/l/itmofs-lab?color=green">
  <img alt="Downloads" src="https://img.shields.io/pypi/dm/itmofs-lab?color=orange">
  <a href="{GH}"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-repo-181717?logo=github"></a>
</p>

<p align="center"><code>pip install itmofs-lab</code></p>

---
"""


def build():
    fams = families()
    by_name = {e.spec.name: e.spec for e in ENTRIES}
    by_entry = {e.spec.name: e for e in ENTRIES}
    n_total = len(by_name)

    # ---- sumário geral ----
    sumario = [
        "## 📖 Sumário",
        "",
        "- [Sobre o projeto](#sobre-o-projeto)",
        "- [Destaques](#destaques)",
        "- [Instalação](#instalação)",
        "- [Início rápido](#início-rápido)",
        "- [Conceitos essenciais](#conceitos-essenciais)",
        "- [Exemplos práticos](#exemplos-práticos)",
        "- [Documentação completa dos métodos](#documentação-completa-dos-métodos)",
        "- [Tabela-resumo de todos os métodos](#tabela-resumo-de-todos-os-métodos)",
        "- [Correspondência com a API ITMO_FS](#correspondência-com-a-api-itmo_fs)",
        "- [Compatibilidade](#compatibilidade)",
        "- [Como citar](#como-citar) · [Autor](#autor) · [Licença](#licença)",
        "",
    ]

    about = f"""## Sobre o projeto

A [**ITMO_FS**](https://github.com/ctlab/ITMO_FS) é uma biblioteca rica em métodos
de *feature selection* — filtros, ensembles e wrappers. Mas usá-la exige lidar com
uma API heterogênea: algumas medidas são funções, outras são classes; umas usam
`fit/transform`, outras `run/feature_ranking`; as regras de corte operam sobre
dicionários; e há bugs e requisitos que só aparecem em tempo de execução.

O **itmofs-lab** é uma camada fina, uniforme e documentada por cima da ITMO_FS.
Ele nasceu de um **estudo prático, sistemático e reprodutível** da biblioteca, no
contexto de pesquisa de pós-graduação sobre **Ensemble Feature Selection**: cada
método foi inspecionado em tempo de execução (assinatura real, atributos após
`fit`, requisitos de dados) e exercitado em datasets didáticos, sempre respeitando
a regra de que o conjunto de teste **nunca** participa da seleção. O resultado é
esta biblioteca — que preserva o comportamento nativo da ITMO_FS e apenas padroniza
o uso, sem inventar scores, sem mascarar erros e sem alterar o pacote original.

## Destaques

- 🎯 **API única** — todo método usa `fit` / `transform` e expõe `selected_`,
  `selected_names_` e `scores_`.
- ❓ **Comando de ajuda** — `itmofs-lab info <método>` (ou `m.info()`) mostra
  exatamente **o que entra e o que sai**.
- 🗂️ **Um arquivo por método** — importável isoladamente.
- 🤝 **Honestidade** — métodos que não executam na versão instalada ficam
  **documentados** e levantam um erro claro em vez de falhar de forma obscura.
- 🔬 **Rigor científico** — pensado para evitar *data leakage*.
- 📚 **Documentação completa** — os **{n_total} métodos** documentados abaixo,
  com entradas e saídas.

## Instalação

```bash
pip install itmofs-lab
```

> **⚠️ Ambiente recomendado.** A ITMO_FS 0.3.3 é de ~2021. Para os métodos rodarem
> sem erros de runtime, use dependências compatíveis:
>
> ```bash
> pip install "numpy<2" "pandas<2" "scikit-learn<1.4" itmofs-lab
> ```

## Início rápido

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

## Conceitos essenciais

**1) Comando de ajuda — o que entra e o que sai**

```bash
itmofs-lab list                     # todos os métodos + status
itmofs-lab families                 # métodos agrupados por família
itmofs-lab info gini_index          # o que entra e o que sai deste método
itmofs-lab run gini_index --dataset breast_cancer -k 10
itmofs-lab version
```

No Python: `fs.info("gini_index")`, `fs.list_methods(family="ensembles")`,
`fs.get("chi2_measure").info()`.

**2) Um arquivo por método**

```python
from itmofs_lab.filters.univariate.gini_index import GiniIndex
from itmofs_lab.ensembles.WeightBased import WeightBased

m = GiniIndex(k=10)                 # equivalente a fs.get("gini_index", k=10)
print(GiniIndex.info())
```

**3) Regra científica: anti-leakage**

```text
dataset → split treino/teste → preprocessing.fit(treino) → seletor.fit(treino)
        → transform(treino) e transform(teste) → classificador → avaliação no teste
```

O conjunto de **teste nunca** participa da seleção. Chame `fit` apenas com
`X_train` (e `y_train` quando supervisionado), aplique `transform` ao teste depois,
e escolha `k`/threshold **somente** por validação cruzada no treino.

## Exemplos práticos

**Filtro univariado com regra de corte por percentual**

```python
m = fs.get("f_ratio_measure", cutting_rule="select_best_percentage", cutting_param=0.3)
m.fit(X_tr, y_tr)
print(len(m.selected_), "features escolhidas")
```

**Filtro multivariado (controla redundância) — precisa de dados discretizados**

```python
from sklearn.preprocessing import KBinsDiscretizer
disc = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy="uniform").fit(X_tr)
Xd_tr, Xd_te = disc.transform(X_tr).astype(int), disc.transform(X_te).astype(int)
m = fs.get("MRMR", n_features=10).fit(Xd_tr, y_tr)
print(m.selected_)          # ordem de seleção (sem score global)
```

**Ensemble comparando filtros (fusão de scores)**

```python
m = fs.get("WeightBased", base_measures=["GiniIndex", "FRatio", "ReliefF"], k=10)
m.fit(X_tr, y_tr)
print(m.selected_names_)
```
"""

    # ---- documentação por método ----
    doc = ["## 📚 Documentação completa dos métodos", "",
           f"> **{n_total} métodos** catalogados. Clique para ir à família:", ""]
    for fam in FAMILY_ORDER:
        if fam in fams:
            title = FAMILY_TITLE[fam]
            doc.append(f"- {FAMILY_EMOJI[fam]} [{title}](#{gh_anchor(title)}) — {len(fams[fam])}")
    doc.append("")
    for fam in FAMILY_ORDER:
        if fam not in fams:
            continue
        title = FAMILY_TITLE[fam]
        doc.append(f"### {title}")
        doc.append("")
        doc.append(f"{FAMILY_EMOJI[fam]} *{FAMILY_LEAD[fam]}*")
        doc.append("")
        for name in fams[fam]:
            doc.append(method_block(by_entry[name]))
        doc.append("")

    # ---- tabela-resumo ----
    tbl = ["## 📋 Tabela-resumo de todos os métodos", "",
           "Legenda de status: 🟢 executa · 🟢ad via adaptador · 🟠 dependência ausente · "
           "🔴 indisponível na 0.3.3 · ⚪ apoio.", "",
           "| # | Método | Família | Tipo | Usa `y` | Score | Status |",
           "|---:|---|---|---|:--:|:--:|:--:|"]
    i = 0
    for fam in FAMILY_ORDER:
        for name in fams.get(fam, []):
            i += 1
            s = by_name[name]
            tbl.append(f"| {i} | `{name}` | {fam} | {s.component_type} | "
                       f"{Y_SHORT.get(s.y, s.y)} | {'✅' if s.outputs_scores else '—'} | "
                       f"{STATUS_SHORT.get(s.status, s.status)} |")
    tbl.append("")

    footer = f"""## Correspondência com a API ITMO_FS

Uma reconciliação completa (nos dois sentidos) entre os métodos do `itmofs-lab` e a
API oficial da ITMO_FS — incluindo interfaces internas, regras de corte e
utilitários de apoio — está em
[`docs/CORRESPONDENCIA_API.md`]({GH}/blob/main/docs/CORRESPONDENCIA_API.md).
Resumo: a biblioteca cobre **100%** dos símbolos públicos da API 0.3.2, mais os
extras da 0.3.3 (`anova`, `laplacian_score`).

## Compatibilidade

Alguns métodos presentes na API da ITMO_FS 0.3.3 **não executam** nesta versão
(bugs da biblioteca, dependência ausente, ou design que exige o teste no ajuste).
Eles permanecem **catalogados e documentados**, e ao serem chamados levantam
`NotSupportedError` com o motivo — nada é mascarado.

| Situação | Exemplos |
|---|---|
| 🔴 Bug na biblioteca 0.3.3 | `fit_criterion_measure`, `RecursiveElimination`, `TPhMGWO`, `HillClimbingWrapper`, `AddDelWrapper`, `FilterWrapperHybrid` |
| 🟠 Dependência ausente | `qpfs_filter`, `qpfs_wrapper` (requerem solver de QP) |
| 🔴 Vazamento por design | `SimulatedAnnealing` (exige teste no `fit`) |

## Documentação em site

Além deste README, há um site navegável (MkDocs Material):

```bash
pip install mkdocs mkdocs-material
mkdocs serve      # http://127.0.0.1:8000
```

## Como citar

```bibtex
@software{{santos_itmofs_lab,
  author  = {{Santos, Vinicius de Souza}},
  title   = {{itmofs-lab: interface uniforme e documentada para selecao de caracteristicas com a ITMO_FS}},
  year    = {{2026}},
  url     = {{{GH}}}
}}
```

## Autor

**Vinicius de Souza Santos** — Aluno de pós-graduação, Universidade Estadual
Paulista (UNESP), Rio Claro · ✉️ vinicius-souza.santos@unesp.br

## Licença

Distribuído sob a licença **MIT** (veja [`LICENSE`](LICENSE)). Este pacote é uma
camada de conveniência sobre a [ITMO_FS](https://github.com/ctlab/ITMO_FS), que
possui autores e licença próprios; o `itmofs-lab` não redistribui nem modifica o
código da ITMO_FS.
"""

    content = (HEADER + "\n" + "\n".join(sumario) + "\n" + about + "\n\n"
               + "\n".join(doc) + "\n" + "\n".join(tbl) + "\n" + footer)
    (ROOT / "README.md").write_text(content, encoding="utf-8")
    print(f"README.md: {n_total} métodos, {len(content)} caracteres, {content.count(chr(10))} linhas.")


if __name__ == "__main__":
    build()
