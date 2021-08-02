"""
Module containing decorators that make up Gaya's APIs.
"""
import functools
from typing import Any, Callable, Optional, TypeVar, cast

from loguru import logger
from gaya.dependency_manager import Container
from fastapi import FastAPI
from dependency_injector.wiring import Provide

F = TypeVar("F", bound=Callable[..., Any])


def geometry(
    _func: Optional[F] = None,
    *,
    enable_rest: bool = True,
    app: FastAPI = Provide[Container.app],
) -> Callable[..., Any]:
    def decorator_geometry(func: F) -> F:
        @functools.wraps(func)
        def wrapper_geometry(*args: Any, **kwargs: Any) -> Any:
            logger.debug(f"Making method {func.__name__} accessible as an endpoint.")

            if enable_rest:
                (app.get("/geometry"))(func)

            logger.debug(f"Method {func.__name__} now accessible as an endpoint.")
            return func(*args, **kwargs)

        return cast(F, wrapper_geometry)

    if _func is None:
        return decorator_geometry
    else:
        return decorator_geometry(_func)
