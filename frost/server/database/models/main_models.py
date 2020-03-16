from sqlalchemy import Column, ForeignKey, Integer, String, Text

from frost.server.database.db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    username = Column(String(32), unique=True)
    password = Column(String(128))
    token = Column(String(64), unique=True)

    def __init__(self, username=None, password=None, token=None):
        self.username = username
        self.password = password
        self.token = token

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)

    name = Column(String(64))
    owner = Column(Integer, ForeignKey('users.id'))


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)

    message = Column(Text)
    from_user = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
