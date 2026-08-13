"""CFR — filters.multivariate.

Maximiza correlação e minimiza redundância.

Status na ITMO_FS 0.3.3: OK
Uso:
    >>> from itmofs_lab.filters.multivariate.CFR import CFR
    >>> m = CFR(n_features=10)
    >>> m.fit(X_train, y_train)          # ajusta SÓ no treino
    >>> X_sel = m.transform(X_test)
    >>> m.selected_, m.selected_names_, m.scores_
    >>> print(CFR.info())              # o que entra e o que sai

Arquivo gerado a partir do catálogo central (scripts/gen_method_files.py).
"""
from __future__ import annotations

from ...core.registry import get as _get, spec as _spec   # noqa: E402

NAME = "CFR"
SPEC = _spec(NAME)


class CFR:
    """Wrapper do método ``CFR``. Instancie e use ``.fit()``/``.transform()``.

    Parâmetros vão direto para o método (ex.: ``CFR(k=10)``). Veja
    ``CFR.info()`` para saber o que entra e o que sai.
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
    """Atalho funcional equivalente a ``CFR(**kwargs)``."""
    return _get(NAME, **kwargs)
