from pydantic import BaseModel

from passman.schemas.password import PasswordSchema


class UserSchema(BaseModel):
    id: int


class UserCreateRequestSchema(BaseModel):
    login: str
    password: str


class UserReturnSchema(UserSchema):
    login: str
    passwords: list[PasswordSchema]
