"""SPEC — filters.sparse.

Spectral Feature Selection.

Status na ITMO_FS 0.3.3: OK_WITH_ADAPTER
Uso:
    >>> from itmofs_lab.filters.sparse.SPEC import SPEC
    >>> m = SPEC(n_features=10)
    >>> m.fit(X_train, y_train)          # ajusta SÓ no treino
    >>> X_sel = m.transform(X_test)
    >>> m.selected_, m.selected_names_, m.scores_
    >>> print(SPEC.info())              # o que entra e o que sai

Arquivo gerado a partir do catálogo central (scripts/gen_method_files.py).
"""
from __future__ import annotations

from ...core.registry import get as _get, spec as _spec   # noqa: E402

NAME = "SPEC"
SPEC = _spec(NAME)


class SPEC:
    """Wrapper do método ``SPEC``. Instancie e use ``.fit()``/``.transform()``.

    Parâmetros vão direto para o método (ex.: ``SPEC(k=10)``). Veja
    ``SPEC.info()`` para saber o que entra e o que sai.
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
    """Atalho funcional equivalente a ``SPEC(**kwargs)``."""
    return _get(NAME, **kwargs)
