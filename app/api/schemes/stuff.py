from pydantic import BaseModel


class Roles(BaseModel):
    quest: str = "quest"
    user: str = "user"
    admin: str = "admin"
