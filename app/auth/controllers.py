import uuid

from aiohttp import web

from app.auth.dto import AuthenticateUserDto, CreateUserDto


async def authenticate_user(request, authenticator):
    body = await request.json()

    token = await authenticator.authenticate(
        AuthenticateUserDto(
            username=body.get('username'),
            password=body.get('password')
        )
    )

    return web.json_response({'token': token})


async def register_user(
        request,
        registrar,
        user_mapper,
        auth_user_transformer,
        ):
    body = await request.json()

    user = await registrar.register(
        CreateUserDto(
            id=str(uuid.uuid4()),
            username=body.get('username'),
            password=body.get('password'),
        )
    )

    await user_mapper.create(user)

    return web.json_response(await auth_user_transformer.transform(user))


async def logout_user(request, user_mapper):
    user = await user_mapper.find(request.get('user_id'))

    user.token = None

    await user_mapper.update(user)

    return web.json_response({})
