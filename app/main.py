from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from app.database import Base, engine, SessionLocal
from app.models.category import Category
from app.models.user import User
from app.security import get_password_hash
from app.api.items import router as items_router
from app.api.categories import router as categories_router
from app.api.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Создание категорий
    for name in ["Компьютерные товары", "Товары для дома", "Товары для машины", "Прочее"]:
        if not db.query(Category).filter(Category.name == name).first():
            db.add(Category(name=name))

    # Создание admin
    if not db.query(User).filter(User.username == "admin").first():
        db.add(User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role="admin"
        ))
    db.commit()
    db.close()
    yield


# Создаём приложение
app = FastAPI(title="Склад Товаров", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://warehouse-1-czm8.onrender.com/"],
    allow_credentials=True,
    allow_methods=["https://warehouse-1-czm8.onrender.com/"],
    allow_headers=["https://warehouse-1-czm8.onrender.com/"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Подключаем роутеры
app.include_router(auth_router, prefix="/auth")
app.include_router(items_router)
app.include_router(categories_router)


@app.get("/")
def root():
    return {"message": "Склад запущен! /docs"}