from project import db
from datetime import datetime

from typing import List, Set

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

# task.title
# task.priority
# task.due_date
# task.completed
# task.attachments

# task.user

# task.children

class Task(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(TASK_TITLE_MAX_LENGTH))
    desc: Mapped[str] = mapped_column(db.String(TASK_DESC_MAX_LENGTH))
    priority: Mapped[int] = mapped_column(db.Integer)
    due_date: Mapped[db.DateTime] = mapped_column(db.DateTime)
    completed: Mapped[bool] = mapped_column(db.Boolean, default=False)
    archived: Mapped[bool] = mapped_column(db.Boolean, default=False)

    categories: Mapped[Set["Category"]] = relationship(secondary=category_association_table)
    tags: Mapped[Set["Tag"]] = relationship(secondary=tag_association_table)

    attachments: Mapped[List["Attachment"]] = relationship(back_populates="task")

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")

    parent_id: Mapped[int] = mapped_column(ForeignKey("task.id"), nullable=True)
    children = relationship("Task")

    completed = db.Column(db.Boolean, default=False)  
    completion_date = db.Column(db.DateTime)  
    restored = db.Column(db.Boolean, default=False)

CATEGORY_MAX_LENGTH = 100

class Category(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(CATEGORY_MAX_LENGTH), unique=True)

TAG_MAX_LENGTH = 30

class Tag(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(TAG_MAX_LENGTH), unique=True)


ATTACHMENT_MAX_FILE_NAME_LENGTH = 100

class Attachment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(ATTACHMENT_MAX_FILE_NAME_LENGTH))
    
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    task: Mapped["Task"] = relationship(back_populates="attachments")
