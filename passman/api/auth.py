from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import scoped_session
from starlette.requests import Request

from passman.core.database import get_session
from passman.models.user import User

SECRET_KEY = "ea437c89632bf4b9b925e08636ddb98e646f11e987a3d82d602070b31613b445"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 1800


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    id: int


class UserLoginRequestSchema(BaseModel):
    login: str
    password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_current_user(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(await oauth2_scheme(request), SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            print("1")
            raise credentials_exception
    except JWTError:
        print("2")
        raise credentials_exception
    db = next(get_session())
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        print("3")
        raise credentials_exception
    return user


def authenticate_user(data: UserLoginRequestSchema, db: scoped_session):
    user = db.query(User).filter(User.login == data.login).first()
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
