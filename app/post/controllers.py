import uuid
from datetime import datetime

from aiohttp import web

from app.post.domain import Post, Comment


async def create_post(request, post_mapper):
    user = request['user']
    body = await request.json()

    post = Post(
        id=str(uuid.uuid4()),
        title=body.get('title', ''),
        content=body.get('content', ''),
        image=body.get('image', ''),
        author_id=user.id,
        created_at=datetime.utcnow()
    )

    await post_mapper.create(post)

    return web.json_response({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'image': post.image,
        'authorId': post.author_id,
        'createdAt': post.created_at.timestamp()
    })


async def get_all_posts(request, post_mapper, comment_mapper):
    posts = await post_mapper.get_all_posts()

    result = []
    for post in posts:
        temp = {
            'id': post[0],
            'title': post[1],
            'content': post[2],
            'image': post[3],
            'createdAt': post[4].timestamp(),
            'authorId': post[5],
            'username': post[6],
            'avatar': post[7],
        }
        comments = await comment_mapper.get_comments_for_post(temp['id'])
        comments = [
            {
                'id': comment[0],
                'content': comment[1],
                'createdAt': comment[2].timestamp(),
                'authorId': comment[3],
                'username': comment[4],
                'avatar': comment[5]
            }
            for comment in comments
        ]
        comments.sort(key=lambda c: c['createdAt'])
        temp['comments'] = comments
        result.append(temp)

    result.sort(key=lambda p: p['createdAt'])
    return web.json_response({
        'posts': result
    })


async def create_comment(request, comment_mapper, ws_pool, logger):
    user = request['user']
    body = await request.json()
    post_id = request.match_info.get('post_id')

    comment = Comment(
        id=str(uuid.uuid4()),
        content=body.get('content', ''),
        author_id=user.id,
        post_id=post_id,
        created_at=datetime.utcnow()
    )

    await comment_mapper.create(comment)

    serialized_comment = {
        'id': comment.id,
        'content': comment.content,
        'authorId': comment.author_id,
        'createdAt': comment.created_at.timestamp(),
        'postId': comment.post_id,
        'username': user.username,
        'avatar': user.avatar
    }

    logger.info(f'Pool: {ws_pool._pool}')
    await ws_pool.broadcast(serialized_comment)

    return web.json_response(serialized_comment)
