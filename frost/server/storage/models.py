import json
from base import Base, Unique


class User(Base):
    __tablename__ = 'users'

    def __init__(self, username, password, id_=None, token=None):
        self.id = id_
        self.username = Unique(username)
        self.password = password
        self.token = token


data = Base.data()
print(data)

user = User('koolaid', 'p43sorcds2shwooop43', 8)
User.update(user)

data = Base.data()
print(data)
