from sqlmodel import Session, create_engine, select, SQLModel

# 사용할 데이터베이스 파일 이름
db_file_name = "blog.db"  
# SQLite 데이터베이스 URL 생성
db_url = f"sqlite:///{db_file_name}"
# SQLite 연결 옵션 설정
db_conn_args = {"check_same_thread": False}  

# 데이터베이스 엔진 생성
# SQLite 데이터베이스와의 연결을 담당
db_engine = create_engine(db_url, connect_args=db_conn_args)

# 데이터베이스 세션 생성
# 세션 객체를 사용해서 데이터베이스 작업을 수행할 수 있음.
# with를 사용해서 사용 종료시 자동으로 세션이 닫힘.
def get_db_session():
    with Session(db_engine) as session:
        yield session

# FastAPI가 처음 시작될 때 테이블을 생성하는 함수
def create_db_and_tables():
    SQLModel.metadata.create_all(db_engine)
