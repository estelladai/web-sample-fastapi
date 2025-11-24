# server.py
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates
from database import create_tables, get_db, User, database
from api import router as api_router
from sqlalchemy.orm import Session

app = FastAPI(
    title="FastAPI Demo 應用程式",
    description="一個完整的 FastAPI Web 應用程式示例",
    version="1.0.0"
)

# 用於 session 加密，請自己換掉
app.add_middleware(SessionMiddleware, secret_key="change-me")

# 靜態文件支援
app.mount("/static", StaticFiles(directory="static"), name="static")

# 包含 API 路由
app.include_router(api_router)

templates = Jinja2Templates(directory="templates")

# ---- 小工具：取得目前登入的 user_id ----
def current_user(request: Request):
    return request.session.get("user_id")

# ---- 小工具：保護頁面（未登入→導到 login）----
def ensure_login(request: Request) -> RedirectResponse | None:
    if not current_user(request):
        next_path = request.url.path
        return RedirectResponse(url=f"/login?next={next_path}", status_code=303)
    return None

# ---- 登入 / 登出 ----
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request, next: str = "/"):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "title": "登入", "next": next}
    )

@app.post("/login")
async def login_post(
    request: Request,
    account: str = Form(...),
    password: str = Form(...),
    next: str = Form("/")
):
    # 實際的用戶驗證
    user_data = db.get_user_by_username(account)
    if user_data and db.verify_password(password, user_data['hashed_password']):
        request.session["user_id"] = account
        return RedirectResponse(url=next or "/", status_code=303)
    
    # 失敗就回登入（這裡可以加入錯誤訊息）
    return RedirectResponse(url="/login", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user_id", None)
    return RedirectResponse(url="/login", status_code=303)

# ---- 頁面：首頁 / Page1 / Page2（受保護）----
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    guard = ensure_login(request)
    if guard: 
        return guard
    return templates.TemplateResponse(
        "page1.html",
        {"request": request, "title": "首頁 / Page1"}
    )

@app.get("/page1", response_class=HTMLResponse)
async def page1(request: Request):
    guard = ensure_login(request)
    if guard:
        return guard
    return templates.TemplateResponse(
        "page1.html",
        {"request": request, "title": "Page1"}
    )

@app.get("/page2", response_class=HTMLResponse)
async def page2(request: Request):
    guard = ensure_login(request)
    if guard:
        return guard
    return templates.TemplateResponse(
        "page2.html",
        {"request": request, "title": "Page2"}
    )

@app.get("/articles", response_class=HTMLResponse)
async def articles_page(request: Request):
    guard = ensure_login(request)
    if guard:
        return guard
    return templates.TemplateResponse(
        "articles.html",
        {"request": request, "title": "文章管理"}
    )
