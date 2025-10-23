from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user import UserLogin
from app.dependencies import get_db
from app.crud.user import get_user_by_username
from app.security import create_access_token, verify_password

router = APIRouter(tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_in_db = get_user_by_username(db, user.username)

    if not user_in_db or not verify_password(user.password, user_in_db.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль"
        )

    access_token = create_access_token(
        data={"sub": user_in_db.username, "role": user_in_db.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}