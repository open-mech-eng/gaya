from dependency_injector import containers, providers
from fastapi.applications import FastAPI


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    app = providers.Singleton(FastAPI)
