import os
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from ..model.db import get_db, User
from ..core.security import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from ..core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

load_dotenv() # 讀取 .env 檔案
TURNSTILE_SECRET = os.getenv("TURNSTILE_SECRET")

router = APIRouter()

# 設定密碼加密方式
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Pydantic 模型：定義前端傳進來的資料格式，進行資料驗證與設定管理
class UserRegister(BaseModel):
    username: str = Field(..., min_length=4, max_length=20, pattern="^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=8)
    email: EmailStr
    captcha_token: str

class UserLogin(BaseModel):
    username: str
    password: str

def verify_turnstile(token: str):

    if not TURNSTILE_SECRET:
        print("錯誤: 找不到 TURNSTILE_SECRET 環境變數")
        return False

    # Cloudflare 的驗證 API
    response = requests.post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data={
            "secret": TURNSTILE_SECRET, 
            "response": token
        }
    )
    return response.json().get("success", False)

# --- 註冊 API ---
@router.post("/register")
def register(user: UserRegister,  db: Session = Depends(get_db)):
    if not verify_turnstile(user.captcha_token):
        raise HTTPException(status_code=400, detail="驗證碼無效或過期，請重試")
    
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
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. 找尋使用者
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="帳號或密碼錯誤")
    
    # 2. 比對加密密碼 (verify 會自動將明文密碼與雜湊後的密碼做對比)
    if not pwd_context.verify(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="帳號或密碼錯誤")
    # 3. 密碼正確，核發 JWT Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    # return {"message": "登入成功", "username": db_user.username}

@router.get("/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! You are successfully logged in."}