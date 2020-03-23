from typing import Dict, Tuple, Union

from frost.client.objects import Room, User


class Messages:
    """All messages will be stored in an instance of this class.
    """
    all = dict()
    __new = dict()

    @classmethod
    def get_new_msgs(cls) -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
        """Returns new messages saved and moves them over to :code:`all_messages`.

        :return: The new messages
        :rtype: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
        """
        for room_id, msgs in cls.__new.items():

            if room_id in cls.all:
                cls.all[room_id].update(msgs)
            else:
                cls.all[room_id] = msgs

        try:
            return cls.__new
        finally:
            cls.__new = dict()

    @classmethod
    def add_new_msgs(cls, msgs: Dict[str, Dict[str, Union[str, Dict[str, str]]]]) -> None:
        """Save new messages, sorted by room.

        :param msgs: The messages to save
        :type msgs: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
        """
        for msg_id, msg in msgs.items():

            if msg['room']['id'] in cls.__new:
                cls.__new[msg['room']['id']].update({msg_id: msg})
            else:
                cls.__new[msg['room']['id']] = {msg_id: msg}

    @classmethod
    def clear(cls) -> None:
        """Clears :code:`all_messages` and :code:`_new_messages`.
        """
        cls.all = dict()
        cls.__new = dict()


class EventStatus:
    """Stores the current status of all events.
    """
    login = None
    register = None

    join_room = None
    leave_room = None
    create_room = None

    get_room_msgs = None
    get_invite_code = None
    get_room_members = None
    get_all_joined_rooms = None

    @classmethod
    def get_status(cls, item) -> int:
        """Returns the current status and resets it after.

        :return: The current event status
        :rtype: int
        """
        if hasattr(cls, item) and getattr(cls, item) is not None:
            try:
                return getattr(cls, item)
            finally:
                setattr(cls, item, None)


class Memory:
    rooms = dict()

    @classmethod
    def add_rooms(cls, *rooms: Tuple[Dict[str, Union[str, int]]]) -> None:
        cls.rooms.update({
            room['id']: Room(room['id'], room['name']) for room in rooms
        })

    @classmethod
    def add_room_members(cls, room_id: int, *members: Tuple[Dict[str, Union[str, int]]]) -> None:
        cls.rooms[room_id].members.extend(
            User(m['id'], m['username']) for m in members
        )

    @classmethod
    def set_invite_code(cls, room_id: int, invite_code: str) -> None:
        cls.rooms[room_id].invite_code = invite_code
