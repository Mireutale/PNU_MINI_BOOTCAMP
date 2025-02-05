from enum import Enum
from dataclasses import dataclass
from typing import Optional

# 페이지 이동
class PageDir(Enum):
    NEXT = "next"
    PREV = "prev"

# 게시물
@dataclass
class Post:
    id: int
    title: str
    body: str
    created_at: int
    published: bool

# 게시물 출력
@dataclass
class PostsResp:
    posts: list[Post]
    err_msg: str | None = None

# 게시물 생성
@dataclass
class CreatePostReq:
    title: str
    body: str
    publish: bool = False

# 게시물 수정
@dataclass
class UpdatePostReq:
    title: Optional[str] = None
    body: Optional[str] = None
    publish: Optional[bool] = False

