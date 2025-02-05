from fastapi import FastAPI
from enum import Enum
from dataclasses import dataclass
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

"""
Query Parameters로, q에 값을 입력하는 경우와, 입력하지 않는 경우에 따라서
결과가 바뀐다.

Query Parameters는 기본적으로 데이터 타입이 문자열이지만, FastAPI는 핸들러 함수 인자로 정의된 타입에 맞춰
자동으로 변환을 해준다.
아래 코드에서 page는 int로, filter는 str로 nameonly는 bool로 FastAPI가 자동 변환을 수행
"""
@app.get("/products")
# def get_products(q: str | None = None):
#     products = {"products": [{"name": "Product 1"}, {"name": "Product 2"}]}
#     if q:
#         products.update({"q": q})
#     return products

def getProducts(page: int = 1, filter: str|None = None, nameonly: bool = False):
    print(type(filter))
    print(type(nameonly))
    return [{"id": product_id, "name": name}]

"""
Path Parameters를 사용하는 API -> 반드시 product_id에 값이 들어가야 함.
또한 product_id에 타입을 지정할 수 있다.
[http://127.0.0.1:8000/products/파라미터 지정값] 에 접속해서 
product_id에 해당하는 값이 바뀌는 것을 확인할 수 있다.
타입을 지정한 경우, 잘못된 값이 입력되면 HTTP 422 잘못된 변수 값 입력 에러가 발생.

FastAPI는 코드 내에서 먼저 정의된 Path를 우선으로 라우팅을 처리한다.
따라서, get_product 코드위에 first, second, third에 대한 Path를 처리한다면
타입 에러가 발생하지 않는다.
"""
@app.get("/products/first")
def get_first_product():
    return {"name": "Product 1"}

@app.get("/products/second")
def get_first_product():
    return {"name": "Product 2"}

@app.get("/products/third")
def get_first_product():
    return {"name": "Product 3"}


# @app.get("/products/{product_id}")
# def get_product(product_id: int):
#    return {
#        "products": [
#            {"id": product_id, "name": "Product 1"},
#        ]
#    }

"""
핸들러 함수의 인자 중 Path Parameter이 아닌 인자가 정의되는 경우 자동으로
Query Parameter로 해석된다.
아래 코드에서 product_id는 Path Parameter이고, name과 color는
Query Parameter로 해석된다.
Query Parameter의 기본 데이터 타입은 문자열이다.
Query Parameter는 URL의 일부이며 Path Parameter와는 다르게 필수 인자가 아니다.
따라서 Query Parameter의 값은 None이 가능하며 Optional 형태로 타입을 명시하는 것이 좋다.
"""
@app.get("/products/{product_id}")
# def getProducts(product_id: int, name: str = '', color: str=''):
#     return [{"id": product_id, "name": name, "color": color}]

def getProducts(product_id: int, name: str | None = None ):
    if name is None:
        return [{"id": product_id}]
    return [{"id": product_id, "name": name}]

"""
Query Parameter에 기본값을 지정하지 않은 경우에는 필수 입력 인자가 된다.
따라서, 아래 showpicture에 값이 없으면 오류가 발생한다.
"""
@app.get("/products/{product_id}")
def getProducts(product_id: int, showpicture: bool):
    return {"id": product_id, "showpicture": showpicture}

"""
Enum을 사용하여 Path Parameter로 전달할 수 있는 값의 종류를 제한할 수 있다.
아래와 같은 경우, Truck, Sedan, SUV만 들어갈 수 있다.
"""
class CarTypes(str, Enum):
    Truck = "truck"
    Sedan = "sedan"
    SUV = "suv"

@app.get("/cars/{car_type}")
def get_car(car_type: CarTypes):
    return {"car_type": car_type}

"""
로그인과 게시물
"""

@dataclass
class RequestLogin:
    login_id: str
    password: str

@app.post("/auth/login")
def login(req: RequestLogin):
    return req

@dataclass
class RequestAddComment:
    id: int
    title: str
    body: str

"""
Path Parameter로 선언되면 Path Parameter 값에 대응
dataclass 또는 Pydantic과 같은 모델 클래스의 유형인 경우 Request Body로 해석
단일 유형(int, float, str, bool, ..)이고 Path Parameter이 아니면 Query Parameter로 해석
"""
@app.post("/articles/{article_id}/comments")
def add_comments(article_id: int, req: RequestAddComment):
    return {"article_id": article_id, "comment": req}

@app.post("/articles/{article_id}/comments?showauthoronly=true")
def add_comments(article_id: int, req: RequestAddComment, showauthoronly:bool):
    return {"article_id": article_id, "comment": req, "showauthoronly": showauthoronly}

@dataclass
class RespUser:
    id: int
    name: str
    age: int
    email: str

@app.get("/users/{user_id}")
def get_user_profile(user_id: int) -> RespUser:
    return RespUser(id=user_id, name="Song", age = 40, email="")