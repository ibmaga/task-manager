from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Text, func, DateTime, ForeignKey, String
from datetime import datetime

from app.db.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, nullable=False
    )
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="quest")

    # Связь: пользователь может создать несколько задач
    created_tasks: Mapped[list["Tasks"]] = relationship(
        "Tasks", back_populates="creator", primaryjoin="Users.id==Tasks.creator_id"
    )


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Изменяем поле: вместо ссылки на username используем creator_id, который ссылается на Users.id
    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="created")
    date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), server_default=func.now()
    )

    # Отношение к пользователю (создателю)
    creator: Mapped["Users"] = relationship("Users", back_populates="created_tasks")
