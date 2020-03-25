from typing import Dict, Tuple, Union


class Room:
    """Represents a room in a server, storing information about one.

    :param id_: The room's ID
    :type id_: int
    :param name: The room's name
    :type name: str
    :param members: The members a part of the room, defaults to list()
    :type members: Dict[int, 'User'], optional
    """

    def __init__(self, id_: int, name: str, members: Dict[int, 'User'] = dict()) -> None:
        """The constructor method.
        """
        self.id = id_
        self.name = name
        self.members = members

        self._members_joined = dict()
        self._members_left = dict()

    def __repr__(self) -> str:
        return f"<Room id={self.id} name='{self.name}'>"


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

    def __repr__(self) -> str:
        return f"<User id={self.id} username='{self.username}'>"


class Memory:
    """Stores information that needs to be passed around and easily accessible.
    """
    rooms = dict()
    """The rooms in a server.
    """
    member_changes = {
        'left': {},
        'joined': {}
    }
    """New members which have just joined a room or \
    members who have just left the room, grouped by room.
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
        new_members = {
            m['id']: User(m['id'], m['username']) for m in members
        }
        cls.rooms[room_id].members.update(new_members)

        if cls.member_changes['joined'].get(room_id) is None:
            cls.member_changes['joined'][room_id] = cls.rooms[room_id]

        cls.member_changes['joined'][room_id]._members_joined.update(new_members)

    @classmethod
    def remove_room_member(cls, room_id: int, user_id: int) -> None:
        """Remove a room member who left stored in a room.

        :param room_id: The room's ID the user left from
        :type room_id: int
        :param user_id: The ID of the user who left
        :type user_id: int
        """
        member = cls.rooms[room_id].members[user_id]
        cls.rooms[room_id].members.pop(user_id)

        if cls.member_changes['left'].get(room_id) is None:
            cls.member_changes['left'][room_id] = cls.rooms[room_id]

        cls.member_changes['left'][room_id]._members_left[user_id] = member

    @classmethod
    def get_room_member_changes(cls) -> Dict[str, Dict[int, 'Room']]:
        """Get changes in whether a members left or joined rooms.

        :return: Room member changes
        :rtype: Dict[str, Dict[int, 'Room']]
        """
        try:
            return cls.member_changes
        finally:
            cls.member_changes = {
                'left': {},
                'joined': {}
            }

    @classmethod
    def set_invite_code(cls, room_id: int, invite_code: str) -> None:
        """Store the invite code of a specific room.

        :param room_id: The ID of the room that the invite code corresponds to
        :type room_id: int
        :param invite_code: The invite code to store
        :type invite_code: str
        """
        cls.rooms[room_id].invite_code = invite_code
