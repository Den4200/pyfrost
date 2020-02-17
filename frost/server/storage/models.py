import json
from base import Base


class User(Base):
    __tablename__ = 'users'

    def __init__(self, id_, username, password, token=None):
        self.id = id_
        self.username = username
        self.password = password
        self.token = token


# data = Base.data()
# print(data)

# user = User(3, 'joe', 'password')
# User.update(user)

# data = Base.data()
# print(data)
