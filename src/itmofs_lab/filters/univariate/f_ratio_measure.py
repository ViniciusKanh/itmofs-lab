"""F-ratio (Fisher score) — filters.univariate.

Calcula o Fisher score de cada feature (separação entre classes).

Status na ITMO_FS 0.3.3: OK
Uso:
    >>> from itmofs_lab.filters.univariate.f_ratio_measure import FRatioMeasure
    >>> m = FRatioMeasure(k=10)
    >>> m.fit(X_train, y_train)          # ajusta SÓ no treino
    >>> X_sel = m.transform(X_test)
    >>> m.selected_, m.selected_names_, m.scores_
    >>> print(FRatioMeasure.info())              # o que entra e o que sai

Arquivo gerado a partir do catálogo central (scripts/gen_method_files.py).
"""
from __future__ import annotations

from ...core.registry import get as _get, spec as _spec   # noqa: E402

NAME = "f_ratio_measure"
SPEC = _spec(NAME)


class FRatioMeasure:
    """Wrapper do método ``f_ratio_measure``. Instancie e use ``.fit()``/``.transform()``.

    Parâmetros vão direto para o método (ex.: ``FRatioMeasure(k=10)``). Veja
    ``FRatioMeasure.info()`` para saber o que entra e o que sai.
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
    """Atalho funcional equivalente a ``FRatioMeasure(**kwargs)``."""
    return _get(NAME, **kwargs)
