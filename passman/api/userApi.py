from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import scoped_session

from passman.api.auth import (
    UserLoginRequestSchema,
    authenticate_user,
    create_access_token,
    Token,
    get_current_user,
    get_password_hash
)
from passman.core.database import get_session
from passman.models.user import User
from passman.schemas.user import UserReturnSchema, UserCreateRequestSchema

router = APIRouter()


@router.post('/', response_model=Token)
def create_user(user: UserCreateRequestSchema, db: scoped_session = Depends(get_session)) -> dict:
    db_user = User(**user.dict())
    db_user.password = get_password_hash(db_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token({'id': db_user.id})
    return Token(access_token=access_token)


@router.post('/login', response_model=Token)
def login_user(data: UserLoginRequestSchema, db: scoped_session = Depends(get_session)):
    user = authenticate_user(data, db)
    access_token = create_access_token({'id': user.id})
    return Token(access_token=access_token)


@router.get("/me", response_model=UserReturnSchema)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.delete('/me')
def delete_user(current_user: User = Depends(get_current_user), db: scoped_session = Depends(get_session)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404)
    db.delete(user)
    db.commit()
    return {"id": user.id}
