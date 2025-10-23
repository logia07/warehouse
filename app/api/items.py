# app/api/items.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.item import Item
from app.models.category import Category
from app.schemas.item import ItemBase, ItemCreate
from app.dependencies import get_db, get_current_user, get_admin_user

router = APIRouter(prefix="/items", tags=["items"])


# ✅ GET /items/ - Получить список товаров
@router.get("/", response_model=list[ItemBase])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получает список всех товаров.
    """
    return db.query(Item).offset(skip).limit(limit).all()


# ✅ POST /items/ - Создать новый товар
@router.post("/", response_model=ItemBase)
def create_item(
        item: ItemCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    Создаёт новый товар и привязывает к указанным категориям.
    Только авторизованный пользователь может создать товар.
    """
    # Создаём товар без категорий
    db_item = Item(name=item.name, price=item.price, quantity=item.quantity)

    # Привязываем категории, если они указаны
    if item.category_ids:
        categories = db.query(Category).filter(Category.id.in_(item.category_ids)).all()
        if len(categories) != len(item.category_ids):
            missing = set(item.category_ids) - {c.id for c in categories}
            raise HTTPException(
                status_code=404,
                detail=f"Категории не найдены: {list(missing)}"
            )
        db_item.categories = categories

    # Сохраняем в базу
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# ✅ DELETE /items/{item_id} - Удалить товар (только для admin)
@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user=Depends(get_admin_user)):
    """
    Удаляет товар по ID. Только пользователи с ролью 'admin' могут удалять.
    """
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Товар не найден")

    db.delete(db_item)
    db.commit()
    return {"detail": "Удалён"}