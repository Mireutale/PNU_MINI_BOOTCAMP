from fastapi import (
    FastAPI,HTTPException,status,Depends
)
import time
from dataclasses import dataclass, asdict
from sqlmodel import (
    Field, SQLModel,
    Session, create_engine, select
)

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

# SQLite 데이터베이스 URL 생성
db_url = 'sqlite:///blog.db'

# 데이터베이스 엔진 생성
# SQLite 데이터베이스와의 연결을 담당
db_engine = create_engine(db_url,
        connect_args={"check_same_thread": False})

# 데이터베이스 세션 생성
# 세션 객체를 사용해서 데이터베이스 작업을 수행할 수 있음.
# with를 사용해서 사용 종료시 자동으로 세션이 닫힘.
def get_db_session():
    with Session(db_engine) as session:
        yield session

# FastAPI가 처음 시작될 때 테이블을 생성하는 함수
def create_db():
    SQLModel.metadata.create_all(db_engine)

app = FastAPI()
# db 테이블 생성
create_db()

# Depends를 통해서 데이터베이스 세션 return값인 세션을 자동으로 db에 입력
# post에서는 post에 JSON데이터를 받아서 객체로 변환
@app.post("/posts")
def create_post(post: PostReq,
                db = Depends(get_db_session)):
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

# get을 통해서 page에 대한 게시물을 받음
# page의 기본 값은 1, limit의 기본값은 2
@app.get("/posts")
def get_posts(page: int=1, limit: int=2,
              db=Depends(get_db_session)):
    # page가 1보다 작은 경우 1로 고정
    if page < 1:
        page = 1
    # limit가 1보다 작은경우 빈 리스트를 반환
    if limit < 1:
        return []
    
    # 요청된 페이지 번호와 표시할 게시물의 개수를 nOffset으로 설정
    nOffset = (page-1) * limit

    # db에서 nOffset위치부터 limit개수만큼 데이터를 불러옴
    # 이후 all을 사용해서 쿼리 결과를 리스트 형태로 반환
    posts = db.exec(
        select(Post).offset(nOffset).limit(limit)
    ).all()
    # 리스트 출력
    return posts

# path parameter사용
@app.get("/posts/{post_id}")
def get_post(post_id: int, db=Depends(get_db_session)):
    # db에서 Post 데이터클래스와 매핑된 모델의 post_id와 동일한 값을 불러옴
    post = db.get(Post, post_id)
    # 만약 조회된 게시물이 없는 경우 HTTP예외를 발생
    if not post:
        raise HTTPException(status_code=404,
                            detail="Not Found")
    # 조회된 게시물이 있는 경우 게시물을 출력
    return [post]

# path parameter사용 게시물 삭제
@app.delete("/posts/{post_id}")
def post_delete(post_id: int,
                db=Depends(get_db_session())):
    post = db.get(Post, post_id)
    if not post:
            raise HTTPException(status_code=404,
                                detail="not found")
    db.delete(post)
    db.commit()
    return {
        'ok' : True
    }

@app.put("/posts/{posts_id}")
def update_post(post_id:int,
                reqBody: PostReq,
                db=Depends(get_db_session())):
    oldPost = db.get(Post, post_id)
    if not oldPost:
        raise HTTPException(status_code=404,
                            detail="not found")
    # title, body, published를 가진 데이터 클래스 객체 reqBody
    # asdict을 사용해서 딕셔너리로 변환
    dictToUpdate = asdict(reqBody)
    # oldPost의 객체를 업데이트
    oldPost.sqlmodel_update(dictToUpdate)
    db.add(oldPost)
    db.commit()
    db.refresh(oldPost)
    return oldPost








