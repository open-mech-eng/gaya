"""Console script for gaya."""
import click
from gaya.gaya import main
from loguru import logger


@click.group()
def cli():
    pass


@click.command()
@click.argument("import_path", nargs=1, type=str)
@logger.catch
def run(import_path: str):
    """Run the gaya application at IMPORT_PATH.

    IMPORT_PATH is the python import path of the application class. E.g. module.submodule:MyClass
    """
    main(import_str=import_path)
    return


cli.add_command(run)
