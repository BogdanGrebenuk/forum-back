from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.ws.controllers import index


class WSContainer(containers.DeclarativeContainer):

    application_utils = providers.DependenciesContainer()

    index = ext_aiohttp.View(
        index,
        ws_pool=application_utils.ws_pool
    )
