import json
from typing import Dict, Union


class Messages:
    """All messages will be stored in an instance of this class.
    """
    all = dict()
    __new = dict()

    @staticmethod
    def get_new_msgs() -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
        """Returns new messages saved and moves them over to :code:`all_messages`.

        :return: The new messages
        :rtype: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
        """
        for room_id, msgs in Messages.__new.items():

            if room_id in Messages.all:
                Messages.all[room_id].update(msgs)
            else:
                Messages.all[room_id] = msgs

        try:
            return Messages.__new
        finally:
            Messages.__new = dict()

    @staticmethod
    def add_new_msgs(msgs: Dict[str, Dict[str, Union[str, Dict[str, str]]]]) -> None:
        """Save new messages, sorted by room.

        :param msgs: The messages to save
        :type msgs: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
        """
        for msg_id, msg in msgs.items():

            if msg['room']['id'] in Messages.__new:
                Messages.__new[msg['room']['id']].update({msg_id: msg})
            else:
                Messages.__new[msg['room']['id']] = {msg_id: msg}

    @staticmethod
    def clear() -> None:
        """Clears :code:`all_messages` and :code:`_new_messages`.
        """
        Messages.all = dict()
        Messages.__new = dict()


class EventStatus:
    """Stores the current status of all events.
    """

    @staticmethod
    def get_status(item) -> int:
        """Returns the current status and resets it after.

        :return: The current event status
        :rtype: int
        """
        if hasattr(EventStatus, item) and getattr(EventStatus, item) is not None:
            try:
                return getattr(EventStatus, item)
            finally:
                setattr(EventStatus, item, None)


class Memory:
    invite_codes = dict()
    rooms = list()


if __name__ != "__main__":
    Messages.add_new_msgs({
        1: {
            'message': 'test 1',
            'room': {
                'name': 'test room',
                'id': 1
            },
            'from_user': {
                'username': 'test user',
                'id': 1
            },
            'timestamp': 'todayyyy'
        },
        2: {
            'message': 'test 2',
            'room': {
                'name': 'test room',
                'id': 5
            },
            'from_user': {
                'username': 'test user',
                'id': 1
            },
            'timestamp': 'todayyyy'
        },
        3: {
            'message': 'test 3',
            'room': {
                'name': 'test room',
                'id': 1
            },
            'from_user': {
                'username': 'test user',
                'id': 1
            },
            'timestamp': 'todayyyy'
        },
    })

    print(json.dumps(Messages.get_new_msgs(), indent=2))
    print('\n'*5)

    Messages.add_new_msgs({
        4: {
            'message': 'test 4',
            'room': {
                'name': 'test room',
                'id': 5
            },
            'from_user': {
                'username': 'test user',
                'id': 1
            },
            'timestamp': 'todayyyy'
        },
        5: {
            'message': 'test 5',
            'room': {
                'name': 'test room',
                'id': 1
            },
            'from_user': {
                'username': 'test user',
                'id': 1
            },
            'timestamp': 'todayyyy'
        },
    })

    print(json.dumps(Messages.get_new_msgs(), indent=2))
    print('\n'*5)
    print(json.dumps(Messages.all, indent=2))
