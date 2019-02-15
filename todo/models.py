from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from werkzeug.security import generate_password_hash, check_password_hash

from db import Base, db_session


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password_hash = Column(String)

    # TODO: backref to items?

    def __init__(self, email=None, password=None):
        self.email = email
        self.set_password(password)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# TODO: check defaults/not nulls
class TodoListItem(Base):
    __tablename__ = 'todo_list_items'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_done = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    due_date = Column(DateTime, default=None)

    def __init__(self, text=None, user_id=None, due_date=None):
        self.text = text
        self.user_id = user_id
        self.due_date = due_date

    def save(self):
        db_session.add(self)
        db_session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'text': self.text,
            'is_done': self.is_done,
            'is_hidden': self.is_hidden,
            'due_date': self.due_date
        }