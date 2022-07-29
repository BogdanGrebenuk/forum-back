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
        'author_id': post.author_id,
        'created_at': post.created_at.timestamp()
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
            'created_at': post[4].timestamp(),
            'author_id': post[5],
            'username': post[6],
            'avatar': post[7],
        }
        comments = await comment_mapper.get_comments_for_post(temp['id'])
        comments = [
            {
                'id': comment[0],
                'content': comment[1],
                'created_at': comment[2].timestamp(),
                'author_id': comment[3],
                'username': comment[4],
                'avatar': comment[5]
            }
            for comment in comments
        ]
        comments.sort(key=lambda c: c['created_at'])
        temp['comments'] = comments
        result.append(temp)

    result.sort(key=lambda p: p['created_at'])
    return web.json_response({
        'posts': result
    })


async def create_comment(request, comment_mapper):
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

    return web.json_response({
        'id': comment.id,
        'content': comment.content,
        'author_id': comment.author_id,
        'created_at': comment.created_at.timestamp(),
        'post_id': comment.post_id,
        'username': user.username,
        'avatar': user.avatar
    })
