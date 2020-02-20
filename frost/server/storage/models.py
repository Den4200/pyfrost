import json
from base import Base, Unique


class User(Base):
    __tablename__ = 'users'

    def __init__(self, id_, username, password, token=None):
        self.id = id_
        self.username = Unique(username)
        self.password = password
        self.token = token


# data = Base.data()
# print(data)

# user = User(5, 'boss', 'p43sorcds2shwooop43ool')
# User.add(user)

# data = Base.data()
# print(data)
