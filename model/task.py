from project import db

from typing import List

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

TASK_TITLE_MAX_LENGTH = 400
TASK_DESC_MAX_LENGTH = 2000


category_association_table = Table("category_association_table",
    db.Model.metadata,
    Column("task_id", ForeignKey("task.id"), primary_key=True),
    Column("category_id", ForeignKey("category.id"), primary_key=True))

tag_association_table = Table("tag_association_table",
    db.Model.metadata,
    Column("task_id", ForeignKey("task.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True))


class Task(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(TASK_TITLE_MAX_LENGTH))
    desc: Mapped[str] = mapped_column(db.String(TASK_DESC_MAX_LENGTH))
    priority: Mapped[int] = mapped_column(db.Integer)
    due_date: Mapped[db.DateTime] = mapped_column(db.DateTime)

    categories: Mapped[List["Category"]] = relationship(secondary=category_association_table)
    tags: Mapped[List["Tag"]] = relationship(secondary=tag_association_table)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")

CATEGORY_MAX_LENGTH = 100

class Category(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(CATEGORY_MAX_LENGTH), unique=True)

TAG_MAX_LENGTH = 30

class Tag(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(TAG_MAX_LENGTH), unique=True)


