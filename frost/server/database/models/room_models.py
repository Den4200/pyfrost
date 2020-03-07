from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)
from frost.server.database.db import Base


class RoomMember(Base):
    __tablename__ = 'roommembers'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
