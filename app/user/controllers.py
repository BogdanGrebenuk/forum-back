from aiohttp import web

from app.exceptions.application import DomainException


async def get_user_me(request, user_transformer):
    user = request['user']

    return web.json_response(await user_transformer.transform(user))


async def update_me(request, user_mapper, user_transformer):
    user = request['user']
    body = await request.json()

    new_avatar = body.get('avatar')
    if new_avatar:
        user.avatar = new_avatar

    new_username = body.get('username')
    if new_username:
        user_with_same_username = await user_mapper.find_one_by(username=new_username)
        if (user_with_same_username is not None) and (user.id != user_with_same_username.id):
            raise DomainException('Username is already taken.')
        user.username = new_username

    await user_mapper.update(user)

    return web.json_response(await user_transformer.transform(user))
