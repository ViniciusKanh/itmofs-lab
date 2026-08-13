"""QPFS (wrapper) — wrappers.

Quadratic Programming Feature Selection na forma de wrapper.

Status na ITMO_FS 0.3.3: DEPENDENCY_MISSING
Uso:
    >>> from itmofs_lab.wrappers.qpfs_wrapper import QpfsWrapper
    >>> m = QpfsWrapper()
    >>> m.fit(X_train, y_train)          # ajusta SÓ no treino
    >>> X_sel = m.transform(X_test)
    >>> m.selected_, m.selected_names_, m.scores_
    >>> print(QpfsWrapper.info())              # o que entra e o que sai

Arquivo gerado a partir do catálogo central (scripts/gen_method_files.py).
"""
from __future__ import annotations

from ..core.registry import get as _get, spec as _spec   # noqa: E402

NAME = "qpfs_wrapper"
SPEC = _spec(NAME)


class QpfsWrapper:
    """Wrapper do método ``qpfs_wrapper``. Instancie e use ``.fit()``/``.transform()``.

    Parâmetros vão direto para o método (ex.: ``QpfsWrapper(k=10)``). Veja
    ``QpfsWrapper.info()`` para saber o que entra e o que sai.
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
    """Atalho funcional equivalente a ``QpfsWrapper(**kwargs)``."""
    return _get(NAME, **kwargs)
