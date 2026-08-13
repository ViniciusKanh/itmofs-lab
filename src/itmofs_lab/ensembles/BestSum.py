"""BestSum — ensembles.model_based.

Ensemble model-based: importâncias ponderadas por desempenho de CV (só treino).

Status na ITMO_FS 0.3.3: OK_WITH_ADAPTER
Uso:
    >>> from itmofs_lab.ensembles.BestSum import BestSum
    >>> m = BestSum(k=10)
    >>> m.fit(X_train, y_train)          # ajusta SÓ no treino
    >>> X_sel = m.transform(X_test)
    >>> m.selected_, m.selected_names_, m.scores_
    >>> print(BestSum.info())              # o que entra e o que sai

Arquivo gerado a partir do catálogo central (scripts/gen_method_files.py).
"""
from __future__ import annotations

from ..core.registry import get as _get, spec as _spec   # noqa: E402

NAME = "BestSum"
SPEC = _spec(NAME)


class BestSum:
    """Wrapper do método ``BestSum``. Instancie e use ``.fit()``/``.transform()``.

    Parâmetros vão direto para o método (ex.: ``BestSum(k=10)``). Veja
    ``BestSum.info()`` para saber o que entra e o que sai.
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
    """Atalho funcional equivalente a ``BestSum(**kwargs)``."""
    return _get(NAME, **kwargs)
