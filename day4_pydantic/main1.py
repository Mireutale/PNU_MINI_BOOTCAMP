from pydantic import BaseModel, ValidationError, Json, conint, SecretStr
from typing import Optional, Literal, Callable, Any, List
from datetime import datetime, time, date, timedelta
import json

print(json.dumps(""))

class Addr(BaseModel):
    country: str
    city: str

# * pydantic의 BaseModel을 상속받아서 클래스 생성
class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True
    addr: Optional[Addr] = None

class Shop(BaseModel):
    id: int
    name: str
    addr: Addr

user = User(id = 1, name = "Linux", email = "linux@linux.com")
print(user)
# * json 파일로 데이터 변환
print(user.model_dump_json())
# * dictionary 파일로 데이터 변환
user_dict = user.model_dump()
print(user_dict)

userDict = {
    "id": 99,
    "name": "Linux",
    "email": "aaa@aa.com"
}

# * user4 = User(id = 1, name = "sss", email = "asdsad") 처럼 인식
user4 = User(**userDict)
print(user4)
# * validate -> json을 pydantic모델로 변환
user5 = User.model_validate_json(user.model_dump_json())
print(user5)

class Car(BaseModel):
    color : Literal["red", "green", "blue"]

# * 수행 ㅇ
print(Car(color = "red"))
print(Car(color = "green"))
print(Car(color = "blue"))
# ! 에러발생
try:
    blackCar = Car(color = "black")
except ValidationError as ve:
    print(ve)

class Switch(BaseModel):
    on: bool

s1 = Switch(on = True)
print(s1)
s2 = Switch(on = "on")
print(s2)
s3 = Switch(on = "yes")
print(s3)
s4 = Switch(on = "no")
print(s4)
# # ! 에러발생
# s5 = Switch(on = "hello")
# print(s5)

class Methods(BaseModel):
    # * [입력 매개변수], 출력 매개변수
    # * 함수타입 검증 반드시 int 입력 -> str 출력으로 나와야 함
    on_startup: Callable[[int], str]

def int_to_str(val: int) -> str:
    return f'{val}'

m = Methods(on_startup=int_to_str)
sss = m.on_startup(100)
print(sss)

class DTModel(BaseModel):
    d: date = None
    dt: datetime = None
    t: time = None
    td: timedelta = None

dtModel = DTModel(
    d=1738195200.0,
    dt='2025-01-31T10:20:30.400+09:00',
    t=time(10,12,13),
    td='P3DT12H30M5S'
)
print(dtModel)

class AnyJsonModel(BaseModel):
    json: Json[Any]

class ConstrainedJsonModel(BaseModel):
    json: Json[List[int]]

print(AnyJsonModel(json='{"Hello": 3.14}'))
print(ConstrainedJsonModel(json='[3,1,4]'))

class TestModel(BaseModel):
    age: conint(gt=15, lt=150)

try:
    print(TestModel(age = 20))
    # ! 에러발생
    print(TestModel(age = 200))
except Exception as e:
    print("out of range", e)

class SecretModel(BaseModel):
    login_id: str
    pwd: SecretStr

sm = SecretModel(login_id='linux', pwd='1234')
# * 아래 모든 pwd값은 전부 '***'형태로 숨김 처리가 됨.
# * 실제로 값이 변하는 것은 아님.
print(sm)
print(sm.model_dump())
print(sm.model_dump_json())