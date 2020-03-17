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
        self.all_messages.update(self._new_messages)
        try:
            return self._new_messages
        finally:
            self._new_messages = dict()

    def add_new_msgs(self, msgs: Dict[str, Dict[str, Union[str, Dict[str, str]]]]) -> None:
        """Save new messages.

        :param msgs: The messages to save
        :type msgs: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
        """
        self._new_messages.update(msgs)

    def clear(self) -> None:
        """Clears :code:`all_messages` and :code:`_new_messages`.
        """
        self.all_messages = dict()
        self._new_messages = dict()


class AuthStatus:
    """Stores the current authentication status.
    """

    def __init__(self) -> None:
        """The constructor method.
        """
        self.current_status = None

    def get_status(self) -> int:
        """Returns the current status and resets it after.

        :return: The current authentication status
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

login_status = AuthStatus()
"""An instance of :class:`frost.client.events.events.AuthStatus` for login status.
"""

register_status = AuthStatus()
"""An instance of :class:`frost.client.events.events.AuthStatus` for registration status.
"""
