"""itmofs-lab — wrapper simples e uniforme sobre a biblioteca ITMO_FS.

Uso rápido:

    >>> import itmofs_lab as fs
    >>> fs.list_methods()                      # todos os métodos
    >>> print(fs.info("gini_index"))           # o que entra e o que sai
    >>> m = fs.get("gini_index", k=10)
    >>> m.fit(X_train, y_train)                # ajusta SÓ no treino
    >>> X_sel = m.transform(X_test)            # aplica ao teste
    >>> m.selected_, m.selected_names_, m.scores_

Comando de ajuda na linha de comando:

    $ itmofs-lab list
    $ itmofs-lab info gini_index
    $ itmofs-lab run gini_index --dataset breast_cancer -k 10

A instalação da ITMO_FS é a fonte de verdade; este pacote apenas padroniza o
uso e documenta o que cada método faz, respeitando a regra de que o conjunto de
teste nunca participa da seleção.
"""

from __future__ import annotations

from .core.registry import (
    list_methods, families, spec, info, get, all_specs,
)
from .core.base import FSMethod, NotSupportedError
from .core.spec import MethodSpec, STATUS
from .core import compat

__all__ = [
    "list_methods", "families", "spec", "info", "get", "all_specs",
    "FSMethod", "NotSupportedError", "MethodSpec", "STATUS", "compat",
    "itmo_version", "__version__",
]

__version__ = "0.1.2"


def itmo_version() -> str:
    """Versão da ITMO_FS instalada (fonte de verdade)."""
    return compat.itmo_version()
