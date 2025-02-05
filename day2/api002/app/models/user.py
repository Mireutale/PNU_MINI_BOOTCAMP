# 회원가입
from dataclasses import dataclass
@dataclass
class User:
    login_id: str
    password: str
    name: str

# 로그인
@dataclass
class AuthLoginReq:
    login_id: str
    password: str

# 회원가입, 로그인에 대한 답변
@dataclass
class AuthResponse:
    jwt_token: str | None = None
    err_msg: str | None = None
