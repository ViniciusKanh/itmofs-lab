"""Fit Criterion — filters.univariate.

Critério de ajuste por classe (centros/variâncias).

Status na ITMO_FS 0.3.3: BROKEN_IN_0_3_3
Uso:
    >>> from itmofs_lab.filters.univariate.fit_criterion_measure import FitCriterionMeasure
    >>> m = FitCriterionMeasure()
    >>> m.fit(X_train, y_train)          # ajusta SÓ no treino
    >>> X_sel = m.transform(X_test)
    >>> m.selected_, m.selected_names_, m.scores_
    >>> print(FitCriterionMeasure.info())              # o que entra e o que sai

Arquivo gerado a partir do catálogo central (scripts/gen_method_files.py).
"""
from __future__ import annotations

from ...core.registry import get as _get, spec as _spec   # noqa: E402

NAME = "fit_criterion_measure"
SPEC = _spec(NAME)


class FitCriterionMeasure:
    """Wrapper do método ``fit_criterion_measure``. Instancie e use ``.fit()``/``.transform()``.

    Parâmetros vão direto para o método (ex.: ``FitCriterionMeasure(k=10)``). Veja
    ``FitCriterionMeasure.info()`` para saber o que entra e o que sai.
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
    """Atalho funcional equivalente a ``FitCriterionMeasure(**kwargs)``."""
    return _get(NAME, **kwargs)
