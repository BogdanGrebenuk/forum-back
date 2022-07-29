from dataclasses import dataclass

from app.utils.mapper import Entity


@dataclass
class Post(Entity):
    id: str
    title: str
    content: str
    image: str
    author_id: str


@dataclass
class Comment(Entity):
    id: str
    content: str
    author_id: str
    post_id: str
