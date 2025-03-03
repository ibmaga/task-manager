from pydantic import BaseModel, ConfigDict
from typing import Literal
from enum import Enum


roles = Literal["quest", "user", "admin"]
type_token = Literal["access", "refresh"]
statuses = Literal["created", "at work", "frozen", "cancel", "finished"]


# class Roles(Enum):
#     quest: str = "quest"
#     user: str = "user"
#     admin: str = "admin"
#
#
# class TaskStatus(Enum):
#     created = "created"
#     at_work = "at work"
#     frozen = "frozen"
#     cancel = "cancel"
#     finished = "finished"


class Payload(BaseModel):
    type: type_token
    sub: str
    id: int
    role: roles | str
    iat: int
    exp: int

    model_config = ConfigDict(from_attributes=True)


class Tokens(BaseModel):
    access_token: str
    refresh_token: str = None
    type: str = "Bearer"
