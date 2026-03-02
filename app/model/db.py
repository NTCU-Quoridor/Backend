from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 使用 SQLite 資料庫
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/model/data/test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 定義使用者資料表
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

# 建立資料表
Base.metadata.create_all(bind=engine)

# 取得資料庫連線的工具函式
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()