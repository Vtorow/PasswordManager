import uuid

from pydantic import BaseModel


class PasswordRequestSchema(BaseModel):
    description: str
    login: str
    password: str


class PasswordSchema(BaseModel):
    id: int
    description: str
    login: str
    password: str


class PasswordId(BaseModel):
    id: int