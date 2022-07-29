from sqlalchemy.sql import text

from app.utils.mapper import Mapper


class CommentMapper(Mapper):

    async def get_comments_for_post(self, post_id):
        async with self.engine.acquire() as conn:
            result = await (
                await conn.execute(
                    text("""
                        SELECT
                            comment.id as id, comment.content as content, comment.created_at as created_at, \"user\".id as author_id, \"user\".username as username, \"user\".avatar as avatar
                        FROM comment
                        LEFT JOIN \"user\" ON comment.author_id = \"user\".id
                        WHERE comment.post_id = :post_id
                    """),
                    post_id=post_id
                )
            ).fetchall()
            return result
