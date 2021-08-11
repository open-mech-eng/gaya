"""
Module containing decorators that make up Gaya's APIs.
"""
import functools
from typing import Any, Callable, Optional, TypeVar, cast

from loguru import logger
from gaya.dependency_manager import Container
from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from dependency_injector.wiring import Provide, inject

F = TypeVar("F", bound=Callable[..., Any])


@inject
def geometry(
    _func: Optional[F] = None,
    *,
    enable_rest: bool = True,
    router: APIRouter = Provide[Container.router],
) -> Callable[..., Any]:
    def decorator_geometry(func: F) -> F:
        logger.debug(f"Making method {func.__name__} accessible as an endpoint.")

        @router.get("/geometry")
        @functools.wraps(func)
        async def wrapper_geometry(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        return cast(F, wrapper_geometry)

    if _func is None:
        return decorator_geometry
    else:
        return decorator_geometry(_func)


@inject
def component(
    _cls: Optional[Any] = None,
    *,
    router: APIRouter = Provide[Container.router],
):
    def decorator_component(cls: Any) -> Any:
        logger.debug(f"Making class {cls.__name__} a fastAPI router.")

        @functools.wraps(cls)
        def wrapper_component(*args: Any, **kwargs: Any) -> Any:
            modifiedCls = cbv(router)(cls)
            return modifiedCls(*args, **kwargs)

        return wrapper_component

    if _cls is None:
        return decorator_component
    else:
        return decorator_component(_cls)
