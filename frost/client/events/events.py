import json
from typing import Dict, Union


class Messages:
    """All messages will be stored in an instance of this class.
    """

    def __init__(self) -> None:
        """The constructor method.
        """
        self.all_messages = dict()
        self._new_messages = dict()

    def get_new_msgs(self) -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
        """Returns new messages saved and moves them over to :code:`all_messages`.

        :return: The new messages
        :rtype: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
        """
        for room_id, msgs in self._new_messages.items():

            if room_id in self.all_messages:
                self.all_messages[room_id].update(msgs)
            else:
                self.all_messages[room_id] = msgs

        try:
            return self._new_messages
        finally:
            self._new_messages = dict()

    def add_new_msgs(self, msgs: Dict[str, Dict[str, Union[str, Dict[str, str]]]]) -> None:
        """Save new messages, sorted by room.

        :param msgs: The messages to save
        :type msgs: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
        """
        for msg_id, msg in msgs.items():

            if msg['room']['id'] in self._new_messages:
                self._new_messages[msg['room']['id']].update({msg_id: msg})
            else:
                self._new_messages[msg['room']['id']] = {msg_id: msg}

    def clear(self) -> None:
        """Clears :code:`all_messages` and :code:`_new_messages`.
        """
        self.all_messages = dict()
        self._new_messages = dict()


class EventStatus:
    """Stores the current status of an event.
    """

    def __init__(self) -> None:
        """The constructor method.
        """
        self.current_status = None

    def get_status(self) -> int:
        """Returns the current status and resets it after.

        :return: The current event status
        :rtype: int
        """
        if self.current_status is not None:
            try:
                return self.current_status
            finally:
                self.current_status = None


messages = Messages()
"""An instance of :class:`frost.client.events.events.Messages`.
"""

login_status = EventStatus()
"""An instance of :class:`frost.client.events.events.EventStatus` for login status.
"""

register_status = EventStatus()
"""An instance of :class:`frost.client.events.events.EventStatus` for registration status.
"""


if __name__ == "__main__":
    messages.add_new_msgs({
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

    print(json.dumps(messages.get_new_msgs(), indent=2))
    print('\n'*5)

    messages.add_new_msgs({
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

    print(json.dumps(messages.get_new_msgs(), indent=2))
    print('\n'*5)
    print(json.dumps(messages.all_messages, indent=2))
