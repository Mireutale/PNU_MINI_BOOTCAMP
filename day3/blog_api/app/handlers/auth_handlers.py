from fastapi import APIRouter
from app.models.user import *

router = APIRouter(
    prefix="/v1/auth"
)

@router.post("/signup",status_code=201)
def signup(user: User) -> AuthResponse:
    return AuthResponse(
        jwt_token="sksksksks"
    )

@router.post("/signin")
def signin(user: AuthLoginReq) -> AuthResponse:
    return AuthResponse(
        jwt_token='aaaa'
    )
