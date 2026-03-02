from fastapi import FastAPI
from app.core.config import addMiddleware
from app.routers import auth

app = FastAPI()
addMiddleware(app)
@app.get("/")
def root():
    return {"message": "This is root!"}
@app.get("/api")
def main():
    return {"message": "Hello World"}

# 「引導」路由：將 auth 檔案中的路徑掛載到主程式下
# prefix="/api" 代表之後所有的 API 都會以 /api 開頭，例如 /api/login
#  tags 是在 /docs 中作為分類的標籤
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
