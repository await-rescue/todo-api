from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from db import Base, db_session


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    # TODO: encrypt!
    password_hash = Column(String)


    def __init__(self, email=None, password_hash=None):
        self.email = email
        password_hash = password_hash

    def save(self):
        db_session.add(self)
        db_session.commit()


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