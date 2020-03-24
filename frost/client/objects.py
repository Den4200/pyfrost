from typing import Dict, List, Tuple, Union


class Room:
    """Represents a room in a server, storing information about one.

    :param id_: The room's ID
    :type id_: int
    :param name: The room's name
    :type name: str
    :param members: The members a part of the room, defaults to list()
    :type members: List[int, 'User'], optional
    """

    def __init__(self, id_: int, name: str, members: List[int, 'User'] = list()) -> None:
        """The constructor method.
        """
        self.id = id_
        self.name = name
        self.members = members


class User:
    """Represents a user in a server, storing information about one.

    :param id_: The user's ID
    :type id_: int
    :param username: The user's username
    :type username: str
    """

    def __init__(self, id_: int, username: str) -> None:
        """The constructor method.
        """
        self.id = id_
        self.username = username


class Memory:
    """Stores information that needs to be passed around and easily accessible.
    """
    rooms = dict()
    """The rooms in a server.
    """

    @classmethod
    def add_rooms(cls, *rooms: Tuple[Dict[str, Union[str, int]]]) -> None:
        """Store rooms as :class:`frost.client.objects.Room` objects in :code:`Memory.rooms`.

        :param *rooms: The rooms to store
        :type *rooms: Tuple[Dict[str, Union[str, int]]]
        """
        cls.rooms.update({
            room['id']: Room(room['id'], room['name']) for room in rooms
        })

    @classmethod
    def add_room_members(cls, room_id: int, *members: Tuple[Dict[str, Union[str, int]]]) -> None:
        """Store members within a room stored in :code:`Memory.rooms`.

        :param room_id: The ID of the room to store the members in
        :type room_id: int
        """
        cls.rooms[room_id].members.extend(
            User(m['id'], m['username']) for m in members
        )

    @classmethod
    def set_invite_code(cls, room_id: int, invite_code: str) -> None:
        """Store the invite code of a specific room.

        :param room_id: The ID of the room that the invite code corresponds to
        :type room_id: int
        :param invite_code: The invite code to store
        :type invite_code: str
        """
        cls.rooms[room_id].invite_code = invite_code
