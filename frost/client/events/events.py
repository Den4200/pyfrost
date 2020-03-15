import time


class Messages:

    def __init__(self) -> None:
        self.all_messages = dict()
        self._new_messages = dict()

    def get_new_msgs(self):
        self.all_messages.update(self._new_messages)
        try:
            return self._new_messages
        finally:
            self._new_messages = dict()

    def add_new_msgs(self, msgs):
        self._new_messages.update(msgs)


class AuthStatus:

    def __init__(self) -> None:
        self.current_status = None

    def get_status(self) -> int:
        while self.current_status is None:
            time.sleep(0.25)

        try:
            return self.current_status
        finally:
            self.current_status = None


messages = Messages()
login_status = AuthStatus()
register_status = AuthStatus()
