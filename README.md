# Wall_Go Backend

[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-05998b.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat&logo=python)](https://www.python.org/)


## 專案總覽 (Project Overview)
這是一個基於 FastAPI 開發的後端系統，主要負責處理 :
- 使用者註冊（含 Cloudflare Turnstile 驗證）
- 使用者登入（OAuth2 Password Form）
- JWT 存取權杖核發與受保護資源驗證
- SQLite 資料持久化（SQLAlchemy ORM）

## 系統架構說明

### 模組職責劃分
- main.py
    - 建立 FastAPI app
    - 註冊 CORS middleware
    - 掛載 auth router 到 /api
- app/core/config.py
    - CORS 設定
    - JWT 相關常數與 Turnstile Secret（目前為程式內預設值）
- app/core/email.py
    - 忘記密碼與密碼重設
- app/core/security.py
    - JWT 建立與解析
    - 受保護路由依賴 get_current_user
    - 建立重設密碼的 token 
- app/model/db.py
    - 資料庫連線（SQLite）
    - User ORM model
    - Session 依賴注入 get_db
- app/routers/auth.py
    - /register, /login, /me API 實作
    - /forgot-password, /reset-password API 實作

### 系統資料流程圖 (Simplified DFD)
![系統資料流程圖](document/DataFlowDiagram.png)

## 帳號密碼規範 (Validation)
為了確保系統安全性，後端針對帳號與密碼設有嚴格的 Pydantic 校驗規則：

1. 帳號名稱 (Username)  
   帳號名稱必須符合以下格式要求，否則系統將回傳驗證錯誤：

    * 字數限制：長度必須介於 4 到 20 個字元 之間。
    * 字元限制：僅允許使用 大、小寫英文字母 (A-Z, a-z)、數字 (0-9) 以及 底線 (_)。
    * 不允許規則：禁止使用空格、特殊符號（如 @, !, # 等）或中文字元。

2. 密碼 (Password)  
為了保護您的帳戶安全，密碼必須符合以下最低要求：

    * 字數限制：長度必須 至少為 8 個字元。

    * 安全建議：雖然系統僅強制檢查長度，但強烈建議密碼應包含 大小寫字母混合、數字 及 特殊符號，以提高安全性。

    * 存儲機制：系統不會以明文方式儲存您的密碼，所有密碼在進入資料庫前皆會經過高強度的雜湊演算法 (Hashing) 處理。

## 資料夾結構說明
```
Backend
├─ app
│  ├─ core                  # 設定檔
│  │  ├─ config.py          #
│  │  ├─ email.py           #
│  │  ├─ security.py        #
│  │  └─ __init__.py        #
│  ├─ model                 #
│  │  ├─ data               #
│  │  ├─ db.py              #
│  │  └─ __init__.py        #
│  ├─ routers               # 使用者 API
│  │  ├─ auth.py            #
│  │  └─ __init__.py        #
│  └─ __init__.py           #
├─ document                 #
│  ├─ APIdocs.png           #
│  ├─ DataFlowDiagram.png   #
│  ├─ diagram               #
│  │  └─ DFD.mdj            #
│  └─ openapi.json          #
├─ frontendTest             #
│  └─ test.html             # 登入及註冊測試網頁
├─ main.py                  # 程式的進入點
├─ README.md                #
└─ requirements.txt         # Python 依賴套件清單
```

* .gitignore
    * 不要上傳 .venv, .env
* /.venv 
    * 由使用者自行建立
* .env 
    * 由使用者自行建立
    * 可複製 .env.example 修改檔名為 .env，並修改當中參數

## 安裝與環境需求 (Installation & Requirements)
### 系統需求
* **Python 版本** : 建議使用 `3.10` 以上版本。
* **套件管理** : 請確保已安裝 `pip`。
* **建議作業系統**：Windows / macOS / Linux

## 快速啟動
以下以 Windows PowerShell 為例：

1. 建立虛擬環境

    ```powershell
    python -m venv .venv
    ```
2. 啟用虛擬環境

    ```powershell
    .venv\Scripts\Activate.ps1
    ```
3. 安裝相關套件

    ```powershell
    pip install -r requirements.txt
    ```
    * (optional) vscode 套件
        * SQLite (alexcvzz)
            * 查看資料庫表格
4. 啟動後端

    ```powershell
    uvicorn main:app --reload
    ```
    * 網址列打 `localhost:8000/docs` 可查看有什麼 api 能用
    * 結束虛擬環境   `deactivate`