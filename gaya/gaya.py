"""Main module."""

import sys
from gaya.dependency_manager import Container
from loguru import logger


def main():
    """Main function."""
    logger.info("Starting Gaya")
    container = Container()
    logger.info("Wiring dependencies")
    container.wire(modules=[sys.modules[__name__]])
    logger.info("Running application")
