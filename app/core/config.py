import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
# 設定白名單 (允許的來源)
origins = [
    "http://localhost:5173",  # 允許的前端
    "http://localhost:8080",  # 可以有多個
]

load_dotenv()

class Settings:
    # --- 專案基本設計 ---
    PROJECT_NAME: str = "WallGo"

    # --- JWT 安全設定 ---
    # 建議從 .env 讀取，沒有則使用預設值
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 登入 Token 有效時間
    RESET_TOKEN_EXPIRE_MINUTES: int = 15  # 忘記密碼 Token 有效時間

    # --- Cloudflare Turnstile ---
    TURNSTILE_SECRET: str = os.getenv("TURNSTILE_SECRET", "1x0000000000000000000000000000000AA")

    # --- Gmail SMTP 寄信設定 ---
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")  
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS")
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS")

    # --- 其他設定 ---
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173/")

# 實例化物件，讓別人可以用 from .config import settings
settings = Settings()

# Middleware 邏輯
def addMiddleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],    # 1. 允許誰來？ (白名單) origin
        allow_credentials=["*"],   # 2. 是否允許攜帶憑證 (如 Cookies) True
        allow_methods=["*"],      # 3. 允許什麼動作？ (* 代表 GET, POST, PUT, DELETE 通通可以)
        allow_headers=["*"],      # 4. 允許什麼 Header？ (* 代表通通可以)
        )
