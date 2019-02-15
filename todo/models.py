from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from db import Base, db_session


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password_hash = Column(String)
    authenticated = Column(Boolean, default=False)

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

    # Flask-Login required methods
    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


# TODO: check defaults/not nulls
class TodoListItem(Base):
    __tablename__ = 'todo_list_items'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_done = Column(Boolean)
    is_hidden = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, text=None, user_id=None):
        self.text = text
        self.is_done = False
        self.is_hidden = False
        self.user_id = user_id

    def save(self):
        db_session.add(self)
        db_session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'text': self.text,
            'is_done': self.is_done,
            'is_hidden': self.is_hidden
        }