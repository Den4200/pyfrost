from typing import Dict, Optional, Union


class Messages:
    """All messages will be stored in this class.
    """
    all = dict()
    """All messages stored.
    """
    __new = dict()
    """New, unread messages.
    """

    @classmethod
    def get_new_msgs(cls) -> Dict[int, Dict[str, Dict[str, Union[str, Dict[str, str]]]]]:
        """Returns new, unread messages.

        :return: The new messages
        :rtype: Dict[int, Dict[str, Dict[str, Union[str, Dict[str, str]]]]]
        """
        try:
            return cls.__new
        finally:
            cls.__new = dict()

    @classmethod
    def add_new_msgs(
        cls, msgs: Dict[int, Dict[str, Dict[str, Union[str, Dict[str, str]]]]]
    ) -> None:
        """Save new messages, grouped by room.

        :param msgs: The messages to save
        :type msgs: Dict[int, Dict[str, Dict[str, Union[str, Dict[str, str]]]]]
        """
        for msg_id, msg in msgs.items():

            if msg['room']['id'] in cls.__new:
                cls.__new[msg['room']['id']].update({msg_id: msg})
            else:
                cls.__new[msg['room']['id']] = {msg_id: msg}

            if msg['room']['id'] in cls.all:
                cls.all[msg['room']['id']].update({msg_id: msg})
            else:
                cls.all[msg['room']['id']] = {msg_id: msg}

    @classmethod
    def clear(cls) -> None:
        """Clears :code:`cls.all` and :code:`cls.__new`.
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

    send_msg = None
    get_room_msgs = None
    get_invite_code = None
    get_room_members = None
    get_joined_rooms = None

    @classmethod
    def get_status(cls, item: str) -> Optional[int]:
        """Returns the current status of the specified item \
        and resets it to :code:`None` after.

        :return: The current event status
        :rtype: Optional[int]
        """
        if hasattr(cls, item) and getattr(cls, item) is not None:
            try:
                return getattr(cls, item)
            finally:
                setattr(cls, item, None)
