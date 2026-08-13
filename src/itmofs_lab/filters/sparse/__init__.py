"""Métodos da família filters.sparse."""
from .MCFS import MCFS  # noqa: F401
from .NDFS import NDFS  # noqa: F401
from .RFS import RFS  # noqa: F401
from .SPEC import SPEC  # noqa: F401
from .UDFS import UDFS  # noqa: F401

__all__ = ["MCFS", "NDFS", "RFS", "SPEC", "UDFS"]
