from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Table,
    DateTime
)

from frost.server.database.db import Base


user_room_association = Table(
    """An association from the many-to-many relationship \
    between users and rooms.
    """
    'user_room_association', Base.metadata,
    Column('users', Integer, ForeignKey('users.id')),
    Column('rooms', Integer, ForeignKey('rooms.id'))
)


class User(Base):
    """The User model. :code:`__tablename__ = 'users'`"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    """The user's ID.
    """

    username = Column(String(32), unique=True, nullable=False)
    """The user's username."""

    password = Column(String(128), nullable=False)
    """The user's password."""

    token = Column(String(43), unique=True, nullable=True)
    """The user's authentication token, used after login."""

    joined_rooms = relationship(
        """The different rooms the user has joined."""
        'Room',
        secondary=user_room_association,
        back_populates='users'
    )

    messages = relationship(
        """The messages the user has sent."""
        'Message',
        back_populates='user'
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username='{self.username}'>"


class Room(Base):
    """The Room model. :code:`__tablename__ = 'rooms'`"""
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, nullable=False)
    """The room's ID."""

    name = Column(String(32), unique=True, nullable=False)
    """The room's name."""

    invite_code = Column(String(36), unique=True, nullable=False)
    """The room's invite code."""

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    """The ID of the user who created the room."""

    users = relationship(
        """The users who are have joined the room."""
        'User',
        secondary=user_room_association,
        back_populates='joined_rooms'
    )

    messages = relationship(
        """The messages that have been sent in the room."""
        'Message',
        back_populates='room'
    )

    def __repr__(self) -> str:
        return f"<Room name='{self.name}'>"


class Message(Base):
    """The Message model. :code:`__tablename__ = 'messages'`"""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    """The message's ID."""

    message = Column(Text, nullable=False)
    """The message's contents."""

    timestamp = Column(DateTime, default=datetime.utcnow)
    """The date and time the message was sent."""

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    """The ID of the user who sent the message."""

    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    """The ID of the room the message was sent in."""

    user = relationship(
        """The user who sent the message."""
        'User',
        back_populates='messages'
    )

    room = relationship(
        """The room the message was sent in."""
        'Room',
        back_populates='messages'
    )

    def __repr__(self) -> str:
        return (
            f"<Message user_id={self.user_id} room_id={self.room_id} "
            f"timestamp='{self.timestamp}'>"
        )
