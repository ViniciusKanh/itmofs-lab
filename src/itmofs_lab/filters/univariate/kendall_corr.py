"""Kendall correlation — filters.univariate.

Correlação de sinal (Kendall) de cada feature.

Status na ITMO_FS 0.3.3: OK
Uso:
    >>> from itmofs_lab.filters.univariate.kendall_corr import KendallCorr
    >>> m = KendallCorr(k=10)
    >>> m.fit(X_train, y_train)          # ajusta SÓ no treino
    >>> X_sel = m.transform(X_test)
    >>> m.selected_, m.selected_names_, m.scores_
    >>> print(KendallCorr.info())              # o que entra e o que sai

Arquivo gerado a partir do catálogo central (scripts/gen_method_files.py).
"""
from __future__ import annotations

from ...core.registry import get as _get, spec as _spec   # noqa: E402

NAME = "kendall_corr"
SPEC = _spec(NAME)


class KendallCorr:
    """Wrapper do método ``kendall_corr``. Instancie e use ``.fit()``/``.transform()``.

    Parâmetros vão direto para o método (ex.: ``KendallCorr(k=10)``). Veja
    ``KendallCorr.info()`` para saber o que entra e o que sai.
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
    """Atalho funcional equivalente a ``KendallCorr(**kwargs)``."""
    return _get(NAME, **kwargs)
