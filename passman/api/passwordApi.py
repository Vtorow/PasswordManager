from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import scoped_session

from passman.api.auth import get_current_user
from passman.core.database import get_session
from passman.models.password import Password
from passman.models.user import User
from passman.schemas.password import PasswordSchema, PasswordRequestSchema, PasswordId

router = APIRouter()


@router.post("/", response_model=PasswordSchema)
def create_password(password: PasswordRequestSchema, current_user: User = Depends(get_current_user),
                    db: scoped_session = Depends(get_session)) -> dict:
    db_password = Password(**password.dict(), user_id=current_user.id)
    db.add(db_password)
    db.commit()
    db.refresh(db_password)
    return db_password


@router.put("/{password_id}", response_model=PasswordSchema)
def update_password(password_id: int, data: PasswordRequestSchema, current_user: User = Depends(get_current_user),
                    db: scoped_session = Depends(get_session)):
    db_password = db.query(Password).filter(Password.id == password_id).first()
    if not db_password:
        raise HTTPException(status_code=404)
    db_password.login = data.login
    db_password.description = data.description
    db_password.password = data.password
    db.add(db_password)
    db.commit()
    db.refresh(db_password)
    return db_password


@router.delete("/{password_id}", response_model=PasswordId)
def delete_password(password_id: int, current_user: User = Depends(get_current_user),
                    db: scoped_session = Depends(get_session)):
    db_password = db.query(Password).filter(Password.id == password_id).first()
    if not db_password:
        raise HTTPException(status_code=404)
    db.delete(db_password)
    db.commit()
    return {"id": password_id}

