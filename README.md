# 安裝與啟動
```
pip install fastapi uvicorn jinja2 python-multipart
uvicorn server:app --reload
```
# 功能說明

瀏覽 http://127.0.0.1:8000

# 流程圖

```
使用者 → 輸入網址 /page1
           ↓
     ensure_login() 檢查
           ↓
    沒登入？是 → 導向 /login?next=/page1
           ↓
    使用者登入，寫入 session["user_id"]
           ↓
    自動 redirect 回 /page1
           ↓
    顯示 page1.html
```

# QA
1. 為什麼啟動是 uvicorn server:app --reload 而不是 python server.py?
這是因為使用的是 FastAPI 框架。FastAPI 是基於 ASGI（Asynchronous Server Gateway Interface）的框架，需要 ASGI 服務器來運行，不能直接用 python server.py