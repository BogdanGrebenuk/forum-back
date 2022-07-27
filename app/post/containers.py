from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.post.controllers import create_post


class PostPackageContainer(containers.DeclarativeContainer):

    mappers = providers.DependenciesContainer()

    # controllers

    create_post = ext_aiohttp.View(
        create_post,
        post_mapper=mappers.post_mapper
    )
