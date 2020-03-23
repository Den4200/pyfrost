class Room:

    def __init__(self, id_, name, members=list()) -> None:
        self.id = id_
        self.name = name
        self.members = members


class User:

    def __init__(self, id_, username):
        self.id = id_
        self.username = username
