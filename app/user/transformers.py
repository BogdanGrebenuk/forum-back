from app.user.domain import User
from app.utils.transformer import Transformer


class UserTransformer(Transformer):

    async def transform(self, user: User):
        return {
            "id": user.id,
            "username": user.username,
            "avatar": user.avatar
        }
