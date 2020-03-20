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

    messages = relationship(
        'Message',
        back_populates='user'
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username='{self.username}'>"


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String(32), unique=True, nullable=False)
    invite_code = Column(String(36), unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    users = relationship(
        'User',
        secondary=user_room_association,
        back_populates='joined_rooms'
    )

    messages = relationship(
        'Message',
        back_populates='room'
    )

    def __repr__(self) -> str:
        return f"<Room name='{self.name}'>"


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)

    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)

    user = relationship(
        'User',
        back_populates='messages'
    )

    room = relationship(
        'Room',
        back_populates='messages'
    )

    def __repr__(self) -> str:
        return (
            f"<Message user_id={self.user_id} room_id={self.room_id} "
            f"timestamp='{self.timestamp}'>"
        )


if __name__ == "__main__":
    # Base.metadata.create_all(bind=engine)
    # db_session.add_all([
    #    User(
    #        username='test',
    #        password='pw'
    #    ),
    #    User(
    #        username='tester',
    #        password='pw'
    #    ),
    #    User(
    #        username='f1re',
    #        password='pw'
    #    ),
    #    Room(
    #        name='pydis',
    #        invite_code='abc123',
    #        owner_id=3
    #    ),
    #    Message(
    #        message='this is a test',
    #        user_id=3,
    #        room_id=1
    #    )
    # ])

    # u = db_session.query(User).all()
    # r = db_session.query(Room).all()
    # u[2].joined_rooms.append(r[0])

    # db_session.commit()

    # u = db_session.query(User).all()
    # r = db_session.query(Room).all()
    # u[2].joined_rooms.append(r[0])
    # print(u[2].joined_rooms)
    # print(r[0].users)
    # db_session.commit()
    pass
