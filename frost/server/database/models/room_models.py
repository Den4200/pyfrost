from sqlalchemy import Column, ForeignKey, Integer

from frost.server.database.db import Base


class RoomMember(Base):
    __tablename__ = 'roommembers'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
