# api.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import get_db, User, Article
import database

router = APIRouter(prefix="/api", tags=["api"])

# Pydantic 模型
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    
    class Config:
        from_attributes = True

class ArticleCreate(BaseModel):
    title: str
    content: str

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    
    class Config:
        from_attributes = True

# API 路由
@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 檢查用戶是否已存在
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用戶名已存在")
    
    # 創建新用戶
    hashed_password = database.hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/articles/", response_model=ArticleResponse)
async def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(
        title=article.title,
        content=article.content,
        author_id=1  # 暫時設為 1，實際應該從認證中取得
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.get("/articles/", response_model=List[ArticleResponse])
async def get_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    return articles