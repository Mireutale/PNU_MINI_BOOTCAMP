from fastapi import APIRouter
from app.models.post import *
from app.models.shared import *
import time

#prefix는 이 라우터 밑에 연결된 URL에 전부 앞에 auth를 붙임.
router = APIRouter(
    prefix="/v1/posts"
)

# 30개의 게시글 출력
# /posts/ == /posts
@router.get("/", status_code=200)
def get_posts(dir: PageDir=PageDir.PREV, 
              post_id: int=0, 
              limit: int=30) -> PostsResp:
    nCurTimestamp = int(time.time())
    return PostsResp(
        posts=[
            Post(id=1, title="T",body="B",
                 created_at=nCurTimestamp,
                 published=True),
            Post(id=2, title="TT",body="B1",
                 created_at=nCurTimestamp,
                 published=True)
        ]
    )

# 선택한 게시글 출력
# /posts/{post_id}
@router.get("/{post_id}", status_code=200)
def get_post(post_id: int) -> PostsResp:
    nCurTimestamp = int(time.time())
    return PostsResp(
        posts=[
            Post(id=post_id, title="T",body="B",
                 created_at=nCurTimestamp,
                 published=True)
        ]
    )

# 게시글 생성
# /posts
@router.post("/", status_code=201)
def create_post(params: CreatePostReq) -> PostsResp:
    nCurTimestamp = int(time.time())
    return PostsResp(
        posts=[
            Post(id=999, title=params.title,
                 body=params.body,
                 created_at=nCurTimestamp,
                 published=params.publish)
        ]
    )

# 게시글 업데이트
@router.put("/{post_id}", status_code=201)
def update_post(post_id: int, params: UpdatePostReq) ->PostsResp:
    nCurTimestamp = int(time.time())
    return PostsResp(
        posts=[
            Post(id=post_id, title=params.title,
                 body=params.body,
                 created_at=nCurTimestamp,
                 published=params.publish)
        ]
    )

# 게시글 삭제
@router.delete("/{post_id}", status_code=200)
def delete_post(post_id: int) -> ResultReq:
    return ResultReq(ok=True)