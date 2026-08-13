"""Núcleo do itmofs-lab."""
from .spec import MethodSpec, STATUS  # noqa: F401
from . import base, compat  # noqa: F401
from .registry import (  # noqa: F401
    list_methods, families, spec, info, get, all_specs,
)
