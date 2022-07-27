from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.post.controllers import create_post, get_all_posts


class PostPackageContainer(containers.DeclarativeContainer):

    mappers = providers.DependenciesContainer()

    # controllers

    create_post = ext_aiohttp.View(
        create_post,
        post_mapper=mappers.post_mapper
    )

    get_all_posts = ext_aiohttp.View(
        get_all_posts,
        post_mapper=mappers.post_mapper
    )
