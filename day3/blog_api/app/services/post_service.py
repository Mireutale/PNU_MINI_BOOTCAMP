from sqlmodel import Session, select, Field, SQLModel
from dataclasses import dataclass
import time

@dataclass
class PostReq:
    title: str
    body: str
    published: bool

class Post(SQLModel, table=True):
    id: int = Field(primary_key=True)
    created_at: int = Field(index=True)
    published: bool = Field(index=True)
    title: str
    body: str

class PostService:
    def get_host(self, db: Session, post_id: int):
        pass

    def get_post(self, db: Session, page: int = 1):
        pass

    def create_post(self, db: Session, post: PostReq):
        postModel = Post()
        postModel.title = post.title
        postModel.body = post.body
        postModel.created_at = int(time.time())
        postModel.published = post.published
        # 데이터베이스에 추가
        db.add(postModel)
        # 데이터베이스에 추가한 값을 저장
        db.commit()
        # 데이터베이스를 새로 불러옴
        db.refresh(postModel)
        return postModel

    def update_post(self, db: Session, post_id: int, post: PostReq):
        pass

    def delete_post(self, db: Session, post_id: int):
        pass
