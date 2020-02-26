from .base import Base, Unique


class User(Base):
    __tablename__ = 'users'

    def __init__(self, username, password, id_=None, token=None):
        self.id = id_
        self.username = Unique(username)
        self.password = password
        self.token = token


class Room(Base):
    __tablename__ = 'rooms'

    def __init__(self, name, owner_id, id_=None, members=[]):
        self.name = Unique(name)
        self.owner_id = owner_id
        self.members = members
        self.id = id_


class Message(Base):
    __tablename__ = 'messages'

    def __init__(self, message, timestamp, from_user, id_=None):
        self.message = message
        self.from_user = from_user
        self.timestamp = timestamp
        self.id = id_
