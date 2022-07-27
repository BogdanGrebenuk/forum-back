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


async def get_all_posts(request, post_mapper):
    posts = await post_mapper.get_all_posts()

    result = []
    for post in posts:
        temp = {
            'id': post[0],
            'title': post[1],
            'content': post[2],
            'image': post[3],
            'author_id': post[4],
            'username': post[5],
            'avatar': post[6],
            'comments': []
        }
        result.append(temp)

    return web.json_response({
        'posts': result
    })
