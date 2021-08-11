from dependency_injector import containers, providers
from fastapi import FastAPI, APIRouter


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    app = providers.ThreadSafeSingleton(FastAPI)

    router = providers.ThreadSafeSingleton(APIRouter)
