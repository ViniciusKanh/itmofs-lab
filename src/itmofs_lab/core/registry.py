"""Registro central: lista, consulta e instancia métodos a partir do catálogo."""

from __future__ import annotations

from .catalog import ENTRIES
from .spec import MethodSpec

# nome -> Entry
_BY_NAME = {e.spec.name: e for e in ENTRIES}


def list_methods(family: str | None = None, status: str | None = None) -> list[str]:
    """Nomes de métodos, opcionalmente filtrados por família (prefixo) e status."""
    out = []
    for e in ENTRIES:
        if family and not e.spec.family.startswith(family):
            continue
        if status and e.spec.status != status:
            continue
        out.append(e.spec.name)
    return sorted(out)


def families() -> dict[str, list[str]]:
    """Mapa família -> métodos."""
    fam: dict[str, list[str]] = {}
    for e in ENTRIES:
        fam.setdefault(e.spec.family, []).append(e.spec.name)
    return {k: sorted(v) for k, v in sorted(fam.items())}


def spec(name: str) -> MethodSpec:
    if name not in _BY_NAME:
        raise KeyError(f"método desconhecido: {name!r}. Use list_methods().")
    return _BY_NAME[name].spec


def info(name: str) -> str:
    """Texto de ajuda (o que entra/o que sai) de um método."""
    return spec(name).io_text()


def get(name: str, **overrides):
    """Instancia um método pronto para .fit()/.transform(), com overrides de params.

    Ex.: get('gini_index', k=15) ; get('WeightBased', base_measures=[...], k=10)
    """
    if name not in _BY_NAME:
        raise KeyError(f"método desconhecido: {name!r}. Use list_methods().")
    e = _BY_NAME[name]
    kwargs = dict(e.kwargs)
    kwargs.update(overrides)
    if e.factory is not None:
        # standalone/sparse recebem a factory
        return e.cls(spec=e.spec, factory=e.factory, **kwargs)
    return e.cls(spec=e.spec, **kwargs)


def all_specs() -> list[MethodSpec]:
    return [e.spec for e in ENTRIES]
