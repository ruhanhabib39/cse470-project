from flask_login import UserMixin
from project import db

from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

EMAIL_MAX_LENGTH = 200
PASSWORD_MAX_LENGTH = 200
NAME_MAX_LENGTH = 300

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String(EMAIL_MAX_LENGTH), unique=True)
    password: Mapped[str] = mapped_column(db.String(PASSWORD_MAX_LENGTH))
    name: Mapped[str] = mapped_column(db.String(NAME_MAX_LENGTH))
    tasks: Mapped[List["Task"]] = relationship(back_populates="user")
    is_confirmed: Mapped[bool] = mapped_column(db.Boolean, default=False)


# current_user.id
# current_user.email
# current_user.tasks
