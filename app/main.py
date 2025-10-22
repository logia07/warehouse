from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app.models.category import Category

# Инициализация категорий
def init_categories(db):
    names = ["Компьютерные товары", "Товары для дома", "Товары для машины", "Прочее"]
    for name in names:
        if not db.query(Category).filter(Category.name == name).first():
            db.add(Category(name=name))
    db.commit()

# Lifespan: старт и завершение
@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    init_categories(db)
    db.close()
    yield

# Создание приложения
app = FastAPI(title="Склад Товаров", lifespan=lifespan)

# Подключаем роутеры
from app.api.items import router as items_router
from app.api.categories import router as categories_router

app.include_router(items_router)
app.include_router(categories_router)

@app.get("/")
def root():
    return {"message": "Склад запущен! Открой /docs"}