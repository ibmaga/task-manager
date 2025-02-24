from pydantic import BaseModel, ConfigDict, constr
from app.api.schemes.other import roles


class UserReg(BaseModel):
    username: constr(min_length=3)
    password: constr(min_length=6)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: roles | str


class UserFromDB(UserOut):
    password: str


class User(UserReg):
    role: roles | str
