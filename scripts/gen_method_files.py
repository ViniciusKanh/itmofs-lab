"""Gera UM ARQUIVO POR MÉTODO dentro do pacote (cada método usável isoladamente).

Cada arquivo expõe uma classe com o nome do método; instanciá-la devolve o
objeto configurado (mesma API fit/transform/info). Também gera os __init__.py
das subpastas de família exportando as classes.

Execute: python scripts/gen_method_files.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from itmofs_lab.core.registry import ENTRIES  # noqa: E402
from itmofs_lab.core import catalog  # noqa: E402  (garante carga)

FAMILY_DIR = {
    "filters.univariate": "filters/univariate",
    "filters.multivariate": "filters/multivariate",
    "filters.sparse": "filters/sparse",
    "filters.unsupervised": "filters/unsupervised",
    "ensembles.measure_based": "ensembles",
    "ensembles.ranking_based": "ensembles",
    "ensembles.model_based": "ensembles",
    "hybrid": "hybrid",
    "embedded": "embedded",
    "wrappers": "wrappers",
}


def class_name(name: str) -> str:
    if "_" not in name and (name[:1].isupper() or name.isupper()):
        return name  # MRMR, JMI, WeightBased, ...
    return "".join(part.capitalize() for part in name.split("_"))


TEMPLATE = '''"""{display} — {family}.

{summary}

Status na ITMO_FS 0.3.3: {status}
Uso:
    >>> from itmofs_lab.{modpath} import {cls}
    >>> m = {cls}({example_kw})
    >>> m.fit(X_train, y_train)          # ajusta SÓ no treino
    >>> X_sel = m.transform(X_test)
    >>> m.selected_, m.selected_names_, m.scores_
    >>> print({cls}.info())              # o que entra e o que sai

Arquivo gerado a partir do catálogo central (scripts/gen_method_files.py).
"""
from __future__ import annotations

from ...core.registry import get as _get, spec as _spec   # noqa: E402
{extra_import}
NAME = "{name}"
SPEC = _spec(NAME)


class {cls}:
    """Wrapper do método ``{name}``. Instancie e use ``.fit()``/``.transform()``.

    Parâmetros vão direto para o método (ex.: ``{cls}(k=10)``). Veja
    ``{cls}.info()`` para saber o que entra e o que sai.
    """

    name = NAME
    spec = SPEC

    def __new__(cls, **kwargs):
        return _get(NAME, **kwargs)

    @staticmethod
    def info() -> str:
        return SPEC.io_text()

    @staticmethod
    def info_dict() -> dict:
        return SPEC.as_dict()


def build(**kwargs):
    """Atalho funcional equivalente a ``{cls}(**kwargs)``."""
    return _get(NAME, **kwargs)
'''


def default_example_kw(entry) -> str:
    kw = entry.kwargs
    if "k" in kw:
        return "k=10"
    if "n_features" in kw:
        return "n_features=10"
    return ""


def main():
    # depth: pacote itmofs_lab.<family_dir>.<method>  -> subir 3 níveis p/ core
    per_family: dict[str, list[tuple[str, str]]] = {}
    for e in ENTRIES:
        fam = e.spec.family
        subdir = FAMILY_DIR.get(fam)
        if subdir is None:
            print("família sem diretório:", fam); continue
        cls = class_name(e.spec.name)
        depth = subdir.count("/") + 1  # níveis abaixo de itmofs_lab
        rel_core = "." * (depth + 1)   # p/ core
        modpath = subdir.replace("/", ".") + "." + e.spec.name
        content = TEMPLATE.format(
            display=e.spec.display, family=fam, summary=e.spec.summary,
            status=e.spec.status, modpath=modpath, cls=cls,
            example_kw=default_example_kw(e), name=e.spec.name,
            extra_import="",
        )
        # ajusta o número de pontos do import conforme a profundidade real
        content = content.replace("from ...core.registry",
                                  "from " + "." * (depth + 1) + "core.registry")
        fpath = SRC / "itmofs_lab" / subdir / f"{e.spec.name}.py"
        fpath.parent.mkdir(parents=True, exist_ok=True)
        fpath.write_text(content, encoding="utf-8")
        per_family.setdefault(subdir, []).append((e.spec.name, cls))

    # __init__.py por subpasta exporta as classes
    for subdir, items in per_family.items():
        init = SRC / "itmofs_lab" / subdir / "__init__.py"
        lines = [f'"""Métodos da família {subdir.replace("/", ".")}."""']
        for name, cls in sorted(items):
            lines.append(f"from .{name} import {cls}  # noqa: F401")
        lines.append("")
        lines.append("__all__ = [" + ", ".join(f'\"{cls}\"' for _, cls in sorted(items)) + "]")
        init.write_text("\n".join(lines) + "\n", encoding="utf-8")

    total = sum(len(v) for v in per_family.values())
    print(f"Gerados {total} arquivos de método em {len(per_family)} subpastas.")


if __name__ == "__main__":
    main()
