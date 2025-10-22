from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.item import Item
from app.models.category import Category
from app.schemas.item import ItemBase, ItemCreate

router = APIRouter(prefix="/items", tags=["items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ItemBase)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, price=item.price, quantity=item.quantity)

    if item.category_ids:
        categories = db.query(Category).filter(Category.id.in_(item.category_ids)).all()
        if len(categories) != len(item.category_ids):
            missing = set(item.category_ids) - {c.id for c in categories}
            raise HTTPException(status_code=404, detail=f"Категории не найдены: {missing}")
        db_item.categories = categories

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[ItemBase])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Item).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=ItemBase)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return item