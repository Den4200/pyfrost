from sqlalchemy import Column, ForeignKey, Integer, String, Text, Table
# from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from frost.server.database.db import Base


user_room_association = Table(
    'user_room_association', Base.metadata,
    Column('users', Integer, ForeignKey('users.id')),
    Column('rooms', Integer, ForeignKey('rooms.id'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)

    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    token = Column(String(43), unique=True, nullable=True)

    joined_rooms = relationship(
        'Room',
        secondary=user_room_association,
        back_populates='users'
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username='{self.username}'>"


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String(32), nullable=False)
    invite_code = Column(String(36), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    users = relationship(
        'User',
        secondary=user_room_association,
        back_populates='joined_rooms'
    )


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)

    message = Column(Text)
    from_user = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
