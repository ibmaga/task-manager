from pydantic import BaseModel, ConfigDict, constr
from app.api.schemes.other import roles


class UserReg(BaseModel):
    username: constr(min_length=3)
    password: constr(min_length=6)


class UserFromDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    password: str
    role: roles | str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    password: str
    role: roles | str


class User(BaseModel):
    username: str
    password: str
    role: roles | str
