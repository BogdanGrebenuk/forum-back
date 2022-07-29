from app.utils.mapper import Mapper


class PostMapper(Mapper):

    async def get_all_posts(self):
        async with self.engine.acquire() as conn:
            result = await (
                await conn.execute(
                    """
                    SELECT
                        post.id as id, post.title as title, post.content as content, post.image as image, post.created_at as created_at, \"user\".id as author_id, \"user\".username as username, \"user\".avatar as avatar
                    FROM post
                    LEFT JOIN \"user\" ON post.author_id = \"user\".id
                    """
                )
            ).fetchall()
            return result
