from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.api.schemes.other import statuses


class Task(BaseModel):
    name: str
    description: str
    status: statuses = "created"


class TaskFromDB(Task):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creator_id: int
    date: datetime


class TaskUpdate(BaseModel):
    status: statuses
    # updated_at: datetime = datetime.now()


class TaskOutput(Task):
    id: int
    date: datetime
