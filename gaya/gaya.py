"""Main module."""

import sys
from types import ModuleType
from typing import Any, Callable, List, cast
from asgiref.typing import ASGI3Application

from functools import cache
from gaya.dependency_manager import Container
from gaya import api
from loguru import logger
from uvicorn.importer import import_from_string
from uvicorn.main import run


@logger.catch
def main(import_str: str):
    """Main function."""
    logger.info("Starting Gaya")

    container = Container()
    container.check_dependencies()
    logger.info("Registering hook for wiring dependencies")

    fastApiInstance = container.app()
    fastApiRouterInstance = container.router()

    try:
        container.wire(modules=[api])
    except:
        logger.error("Registering install hook failed")
        raise

    try:
        ApplicationClass = cast(Callable[..., Any], import_from_string(import_str))
        instance = ApplicationClass()
    except:
        logger.error(f"importing the root component at {import_str} failed.")
        raise

    try:
        logger.info("starting Gaya server")

        fastApiInstance.include_router(fastApiRouterInstance)
        run(
            cast(ASGI3Application, fastApiInstance),
            host="127.0.0.1",
            port=5000,
            log_level="info",
        )
    except:
        logger.error(f"the server did not start.")
        raise

    logger.info("stopping Gaya application")


@cache
def setup_gaya_deps(modules_to_wire: List[ModuleType] = [api]) -> Container:
    """Setup Gaya dependencies."""
    logger.debug("Creating dependency container")
    container = Container()
    container.check_dependencies()
    logger.debug("Wiring container to inject in ")
    container.wire(modules=modules_to_wire)
    return container
