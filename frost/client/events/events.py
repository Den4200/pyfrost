class Messages:

    def __init__(self) -> None:
        self.all_messages = dict()
        self.new_messages = dict()

    def get_new_msgs(self):
        self.all_messages.update(self.new_messages)
        try:
            return self.new_messages
        finally:
            self.new_messages = dict()


messages = Messages()
