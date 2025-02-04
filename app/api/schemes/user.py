from fastapi.openapi.models import HTTPBearer
from pydantic import BaseModel, ConfigDict
from app.api.schemes.stuff import Roles


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegistration(UserLogin):
    role: str = Roles().quest


class UserFromDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    password: str
    role: str


class User(BaseModel):
    username: str
    password: str
    role: str


class Payload(BaseModel):
    username: str
    role: Roles | str
    exp: float

    model_config = ConfigDict(from_attributes=True)


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "Bearer"
