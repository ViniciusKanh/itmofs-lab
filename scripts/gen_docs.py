"""Gera a documentação completa: um .md por método + índice + mkdocs.yml.

Execute: python scripts/gen_docs.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DOCS = ROOT / "docs"
sys.path.insert(0, str(SRC))

from itmofs_lab.core.registry import ENTRIES, families  # noqa: E402
from itmofs_lab.core.spec import STATUS  # noqa: E402

FAMILY_TITLE = {
    "filters.univariate": "Filtros univariados",
    "filters.multivariate": "Filtros multivariados",
    "filters.sparse": "Filtros esparsos",
    "filters.unsupervised": "Filtros não supervisionados",
    "ensembles.measure_based": "Ensembles (baseados em medida)",
    "ensembles.ranking_based": "Ensembles (baseados em ranking)",
    "ensembles.model_based": "Ensembles (baseados em modelo)",
    "hybrid": "Híbridos",
    "embedded": "Embedded",
    "wrappers": "Wrappers",
}


def method_md(e) -> str:
    s = e.spec
    y_map = {"required": "obrigatório", "optional": "opcional", "not_used": "não usado"}
    pre = []
    if s.requires_discrete:
        pre.append("dados discretizados")
    if s.requires_nonnegative:
        pre.append("dados não negativos (X≥0)")
    if s.recommends_scaling not in ("optional", "none"):
        pre.append(f"escala recomendada: `{s.recommends_scaling}`")
    pre_txt = "; ".join(pre) if pre else "nenhum obrigatório"
    params = "\n".join(f"| `{k}` | {v} |" for k, v in s.params.items()) or "| — | — |"
    outs = []
    outs.append("score por feature ✅" if s.outputs_scores else "sem score global ❌")
    outs.append("ranking ✅" if s.outputs_ranking else "ranking ❌")
    outs.append("subconjunto ✅" if s.outputs_subset else "subconjunto ❌")

    lines = [
        f"# {s.display}  (`{s.name}`)",
        "",
        f"**Família:** `{s.family}` — **tipo:** `{s.component_type}`  ",
        f"**Status na ITMO_FS 0.3.3:** `{s.status}` — {STATUS.get(s.status,'')}",
        "",
        f"{s.summary}",
        "",
        "## O que entra",
        "",
        f"- **X:** {'sim' if s.needs_X else 'não'}",
        f"- **y (rótulos):** {y_map.get(s.y, s.y)}",
        f"- **Pré-processamento:** {pre_txt}",
        "",
        "| parâmetro | descrição |",
        "|---|---|",
        params,
        "",
        "## O que sai",
        "",
        "- " + "\n- ".join(outs),
        f"- **Atributos após `fit`:** `selected_`, `selected_names_`"
        + (", `scores_`" if s.outputs_scores else ""),
        f"- **Transforma treino e teste:** {'sim' if s.transforms_test else 'não'}",
        "",
        "## Assinatura na ITMO_FS",
        "",
        f"```\n{s.itmo_signature}\n```",
    ]
    if s.quirks:
        lines += ["", "## Atenções", "", s.quirks]
    if s.status != "OK" and s.status != "OK_WITH_ADAPTER":
        lines += ["", f"> ⚠️ Este método está **catalogado e documentado**, mas o status "
                  f"`{s.status}` indica que não executa nesta versão. Ver 'Atenções'."]
    # exemplo de uso
    ex_kw = "k=10" if "k" in e.kwargs else ("n_features=10" if "n_features" in e.kwargs else "")
    lines += [
        "", "## Exemplo", "",
        "```python",
        "import itmofs_lab as fs",
        f"m = fs.get('{s.name}'" + (f", {ex_kw}" if ex_kw else "") + ")",
        "m.fit(X_train, y_train)      # ajusta SÓ no treino",
        "X_sel = m.transform(X_test)",
        "print(m.selected_names_)",
        "```",
        "",
        "Ajuda na linha de comando:",
        "",
        "```bash",
        f"itmofs-lab info {s.name}",
        f"itmofs-lab run {s.name} --dataset breast_cancer",
        "```",
        "",
        f"**Referência ITMO_FS:** `{s.references or s.family}`",
        "",
    ]
    return "\n".join(lines)


def main():
    (DOCS / "methods").mkdir(parents=True, exist_ok=True)
    by_name = {e.spec.name: e for e in ENTRIES}

    for e in ENTRIES:
        (DOCS / "methods" / f"{e.spec.name}.md").write_text(method_md(e), encoding="utf-8")

    # índice por família
    idx = ["# Catálogo de métodos", "",
           "Documentação completa de todos os métodos da ITMO_FS acessíveis pelo "
           "itmofs-lab, com **o que entra** e **o que sai** de cada um.", ""]
    fams = families()
    for fam in sorted(fams):
        idx.append(f"## {FAMILY_TITLE.get(fam, fam)}  (`{fam}`)")
        idx.append("")
        idx.append("| método | status | resumo |")
        idx.append("|---|---|---|")
        for name in fams[fam]:
            s = by_name[name].spec
            idx.append(f"| [`{name}`](methods/{name}.md) | `{s.status}` | {s.summary} |")
        idx.append("")
    (DOCS / "catalog.md").write_text("\n".join(idx), encoding="utf-8")

    # mkdocs.yml
    nav_methods = []
    for fam in sorted(fams):
        entries = [f"      - {by_name[n].spec.display}: methods/{n}.md" for n in fams[fam]]
        nav_methods.append(f"    - {FAMILY_TITLE.get(fam, fam)}:\n" + "\n".join(entries))
    mkdocs = f"""site_name: itmofs-lab
site_description: Wrapper simples e uniforme sobre a ITMO_FS (filtros, ensembles, wrappers)
theme:
  name: material
  language: pt
  palette:
    - scheme: default
      primary: teal
  features:
    - navigation.expand
    - content.code.copy
markdown_extensions:
  - admonition
  - toc:
      permalink: true
  - pymdownx.superfences
nav:
  - Início: index.md
  - Catálogo: catalog.md
  - Métodos:
{chr(10).join(nav_methods)}
"""
    (ROOT / "mkdocs.yml").write_text(mkdocs, encoding="utf-8")

    print(f"Docs: {len(ENTRIES)} páginas de método + catalog.md + mkdocs.yml")


if __name__ == "__main__":
    main()
