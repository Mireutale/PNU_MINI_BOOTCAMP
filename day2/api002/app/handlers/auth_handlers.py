from fastapi import APIRouter
from app.models.user  import *
from app.models.shared import *

#prefix는 이 라우터 밑에 연결된 URL에 전부 앞에 auth를 붙임.
router = APIRouter(
    prefix="/v1/auth"
)

# prefix + url
# /auth/signup 이 됨.
@router.post("/signup", status_code=200)
def signup(user: User) -> AuthResponse:
    return AuthResponse(
        jwt_token="sksksksks"
    )

# /auth/signin
@router.post("/signin", status_code=200)
def signin(user: AuthLoginReq) -> AuthResponse:
    return AuthResponse(
        jwt_token='aaaa'
    )