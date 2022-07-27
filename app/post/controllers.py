import uuid
from aiohttp import web

from app.post.domain import Post


async def create_post(request, post_mapper):
    user = request['user']
    body = await request.json()

    post = Post(
        id=str(uuid.uuid4()),
        title=body.get('title', ''),
        content=body.get('content', ''),
        image=body.get('image', ''),
        author_id=user.id,
    )

    await post_mapper.create(post)

    return web.json_response({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'image': post.image,
        'author_id': post.author_id
    })


# async def get_posts(request, post_mapper):
