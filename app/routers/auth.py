from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from ..model.db import get_db, User

router = APIRouter()

# 設定密碼加密方式
# 這裡加上 truncate=True 可以強制處理長度問題，
# 但最重要的是確保 bcrypt 正常運作
# 修改加密方式為 argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Pydantic 模型：定義前端傳進來的資料格式，進行資料驗證與設定管理
class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

# --- 註冊 API ---
@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    # 檢查帳號是否已存在，物件.first() => 資料
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="帳號已被註冊")
    # 2. 檢查信箱是否已存在 (新增這段)
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="此電子信箱已被使用")
    try:
        # 密碼加密
        hashed_pwd = pwd_context.hash(user.password)
        # 存入資料庫
        new_user = User(username=user.username, email=user.email, hashed_password=hashed_pwd)
        db.add(new_user)
        db.commit()
        return {"message": "成功"}
    except Exception as e:
        db.rollback() # 發生錯誤時回滾資料庫
        raise HTTPException(status_code=500, detail="系統發生預期外錯誤")

# --- 登入 API ---
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # 1. 找尋使用者
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="帳號或密碼錯誤")
    
    # 2. 比對加密密碼 (verify 會自動將明文密碼與雜湊後的密碼做對比)
    if not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="帳號或密碼錯誤")
    
    return {"message": "登入成功", "username": db_user.username}