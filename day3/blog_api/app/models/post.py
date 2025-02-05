from enum import Enum
from dataclasses import dataclass
from typing import Optional

class PageDir(Enum):
    NEXT = "next"
    PREV = "prev"

@dataclass
class Post:
    id: int
    title: str
    body: str
    created_at: int
    published: bool

@dataclass
class PostsResp:
    posts: list[Post]
    err_msg: str | None = None

@dataclass
class CreatePostReq:
    title: str
    body: str
    publish: bool = False

@dataclass
class UpdatePostReq:
    title: Optional[str] = None
    body: Optional[str] = None
    publish: Optional[bool] = False

