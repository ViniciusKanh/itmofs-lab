"""Spearman correlation — filters.univariate.

Correlação de Spearman de cada feature com o alvo.

Status na ITMO_FS 0.3.3: OK
Uso:
    >>> from itmofs_lab.filters.univariate.spearman_corr import SpearmanCorr
    >>> m = SpearmanCorr(k=10)
    >>> m.fit(X_train, y_train)          # ajusta SÓ no treino
    >>> X_sel = m.transform(X_test)
    >>> m.selected_, m.selected_names_, m.scores_
    >>> print(SpearmanCorr.info())              # o que entra e o que sai

Arquivo gerado a partir do catálogo central (scripts/gen_method_files.py).
"""
from __future__ import annotations

from ...core.registry import get as _get, spec as _spec   # noqa: E402

NAME = "spearman_corr"
SPEC = _spec(NAME)


class SpearmanCorr:
    """Wrapper do método ``spearman_corr``. Instancie e use ``.fit()``/``.transform()``.

    Parâmetros vão direto para o método (ex.: ``SpearmanCorr(k=10)``). Veja
    ``SpearmanCorr.info()`` para saber o que entra e o que sai.
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
    """Atalho funcional equivalente a ``SpearmanCorr(**kwargs)``."""
    return _get(NAME, **kwargs)
