# apps/core/security.py (接續上方)
import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


# 設定 FastAPI 的 OAuth2 依賴項，指定登入的 API 路徑 (假設是 /api/auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """產生 JWT Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta #utcnow在3.12中被優化過，所以12版的看到刪除線屬正常現象，能用
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    # 使用 SECRET_KEY 進行簽章，確保 Token 不被竄改
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    這是一個 FastAPI Dependency (依賴項)。
    只要 API 掛上這個依賴，就會自動檢查 Header 是否有合法的 Bearer Token。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 嘗試解碼 JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError: # 如果 Token 過期或格式錯誤
        raise credentials_exception
    
    # 這裡通常會再去資料庫查一次使用者是否存在，為了簡化先直接回傳 username
    return username