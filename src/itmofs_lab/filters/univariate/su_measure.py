"""Symmetric Uncertainty — filters.univariate.

Correlação informacional SU(X,Y)=2*I(X;Y)/(H(X)+H(Y)).

Status na ITMO_FS 0.3.3: OK
Uso:
    >>> from itmofs_lab.filters.univariate.su_measure import SuMeasure
    >>> m = SuMeasure(k=10)
    >>> m.fit(X_train, y_train)          # ajusta SÓ no treino
    >>> X_sel = m.transform(X_test)
    >>> m.selected_, m.selected_names_, m.scores_
    >>> print(SuMeasure.info())              # o que entra e o que sai

Arquivo gerado a partir do catálogo central (scripts/gen_method_files.py).
"""
from __future__ import annotations

from ...core.registry import get as _get, spec as _spec   # noqa: E402

NAME = "su_measure"
SPEC = _spec(NAME)


class SuMeasure:
    """Wrapper do método ``su_measure``. Instancie e use ``.fit()``/``.transform()``.

    Parâmetros vão direto para o método (ex.: ``SuMeasure(k=10)``). Veja
    ``SuMeasure.info()`` para saber o que entra e o que sai.
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
    """Atalho funcional equivalente a ``SuMeasure(**kwargs)``."""
    return _get(NAME, **kwargs)
