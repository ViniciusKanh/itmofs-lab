"""WeightBased — ensembles.measure_based.

Ensemble por fusão de SCORES normalizados de filtros base.

Status na ITMO_FS 0.3.3: OK
Uso:
    >>> from itmofs_lab.ensembles.WeightBased import WeightBased
    >>> m = WeightBased(k=10)
    >>> m.fit(X_train, y_train)          # ajusta SÓ no treino
    >>> X_sel = m.transform(X_test)
    >>> m.selected_, m.selected_names_, m.scores_
    >>> print(WeightBased.info())              # o que entra e o que sai

Arquivo gerado a partir do catálogo central (scripts/gen_method_files.py).
"""
from __future__ import annotations

from ..core.registry import get as _get, spec as _spec   # noqa: E402

NAME = "WeightBased"
SPEC = _spec(NAME)


class WeightBased:
    """Wrapper do método ``WeightBased``. Instancie e use ``.fit()``/``.transform()``.

    Parâmetros vão direto para o método (ex.: ``WeightBased(k=10)``). Veja
    ``WeightBased.info()`` para saber o que entra e o que sai.
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
    """Atalho funcional equivalente a ``WeightBased(**kwargs)``."""
    return _get(NAME, **kwargs)
