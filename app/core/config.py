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
    PROJECT_NAME: str = "FastAPI 認證"

    # --- 驗證碼設定 ---
    # 優先讀取 .env，若無則使用 Cloudflare 提供的「公開測試金鑰」
    # 這樣直接 push 到 GitHub，別人也能直接跑測試，且不會洩漏你的私鑰
    TURNSTILE_SECRET: str = os.getenv(
        "TURNSTILE_SECRET", 
        "1x0000000000000000000000000000000AA"
    )

Settings = Settings()

def addMiddleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],    # 1. 允許誰來？ (白名單) origin
        allow_credentials=["*"],   # 2. 是否允許攜帶憑證 (如 Cookies) True
        allow_methods=["*"],      # 3. 允許什麼動作？ (* 代表 GET, POST, PUT, DELETE 通通可以)
        allow_headers=["*"],      # 4. 允許什麼 Header？ (* 代表通通可以)
        )

# --- 新增 JWT 環境變數設定 ---
SECRET_KEY = "your-super-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1