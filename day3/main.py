from fastapi import (
    FastAPI,HTTPException,status,Depends
)
from dataclasses import dataclass, asdict
from app.services.post_service import *
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class PostResp:
    posts: list[Post]
    err_str: str | None = None

db_url = 'sqlite:///blog.db'
db_engine = create_engine(db_url,
        connect_args={"check_same_thread": False})

def get_db_session():
    with Session(db_engine) as session:
        yield session

def create_db():
    SQLModel.metadata.create_all(db_engine)

app = FastAPI()
create_db()

@app.post("/posts")
def create_post(post: PostReq,
                db = Depends(get_db_session),
                postService: PostService = Depends()):
    resp = postService.create_post(db, post)

    return resp

@app.get("/posts")
def get_posts(page: int=1, 
            db=Depends(get_db_session),
            postService: PostService = Depends()) -> PostResp:
    if page < 1:
        page = 1
    resp = PostResp(posts=[])
    resp.posts = postService.get_posts(db, page)
    return resp

@app.get("/posts/{post_id}")
def get_post(post_id: int, 
            db=Depends(get_db_session),
            postService: PostService = Depends()) -> PostResp:
    post = postService.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404,
                            detail="Not Found")
    resp = PostResp(posts=[post])
    return resp

@app.delete("/posts/{post_id}")
def delete_post(post_id: int,
            db=Depends(get_db_session),
            postService: PostService = Depends()):
    
    resultCode = postService.delete_post(db, post_id)
    if resultCode == RESULT_CODE.NOT_FOUND:
        raise HTTPException(status_code=404,
                            detail="not found")
    return {
        'ok': True
    }

@app.put("/posts/{post_id}")
def update_post(post_id:int, 
            reqBody: PostReq,
            db=Depends(get_db_session),
            postService: PostService = Depends()):
    post, code = postService.update_post(db, post_id, reqBody)
    if code == RESULT_CODE.NOT_FOUND:
        raise HTTPException(status_code=404,
                            detail="not found")
    if code == RESULT_CODE.FAILED:
        raise HTTPException(status_code=500,
                            detail="internal server error")
    return post








