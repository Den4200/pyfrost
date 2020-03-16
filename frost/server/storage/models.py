from typing import Dict, List

from frost.server.storage.base import Base, Unique


class User(Base):
    """The user model (:code:`__tablename__ = 'users'`)

    :param username: The user's username
    :type username: str
    :param password: The user's password
    :type password: str
    :param id_: The user's ID, autofilled by :meth:`frost.server.storage.base._get_id` if None
    :type id_: str, optional
    :param token: The user's token, defaults to None
    :type token: str, optional
    """
    __tablename__ = 'users'

    def __init__(
        self,
        username: str,
        password: str,
        id_: str = None,
        token: str = None
    ) -> None:
        """The constructor method.
        """
        self.id = id_
        self.username = Unique(username)
        self.password = password
        self.token = token


class Room(Base):
    """The room model (:code:`__tablename__ = 'rooms'`)

    :param name: The room's name
    :type name: str
    :param owner_id: The ID of the owner of the room
    :type owner_id: str
    :param id_: The room's ID, autofilled by :meth:`frost.server.storage.base._get_id` if None
    :type id_: str, optional
    :param members: The members of the room, defaults to :code:`[]`
    :type members: list, optional
    """
    __tablename__ = 'rooms'

    def __init__(
        self,
        name: str,
        owner_id: str,
        id_: str = None,
        members: List[Dict[str, str]] = list()
    ) -> None:
        """The constructor method.
        """
        self.name = Unique(name)
        self.owner_id = owner_id
        self.members = members
        self.id = id_


class Message(Base):
    """The message model (:code:`__tablename__ = 'messages'`)

    :param message: The message sent from a user
    :type message: str
    :param timestamp: The timestamp the message was sent
    :type timestamp: str
    :param from_user: Information about who sent the message
    :type from_user: Dict[str, str]
    :param id_: The message's ID, \
    autofilled by :meth:`frost.server.storage.base._get_id` if None
    :type id_: str, optional
    """
    __tablename__ = 'messages'

    def __init__(
        self,
        message: str,
        timestamp: str,
        from_user: Dict[str, str],
        id_: str = None
    ) -> None:
        """The constructor method.
        """
        self.message = message
        self.from_user = from_user
        self.timestamp = timestamp
        self.id = id_
