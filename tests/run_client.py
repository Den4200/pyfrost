from dataclasses import dataclass

from frost import FrostClient
from frost.client.socketio import threaded

@dataclass
class Messages:
    contents = dict()


# Store messages in memory globally
messages = Messages()


@threaded(daemon=True)
def listen(client: 'FrostClient') -> None:
    while True:
        msgs = client.get_new_msgs()

        if msgs:
            for msg_id, msg in msgs.items():
                messages.contents[msg_id] = msg

            print(messages.contents)


@threaded()
def send_msg(client: 'FrostClient'):
    while True:
        msg = input('> ')
        client.send_msg(msg)


def run_client():
    # with FrostClient() as client:
    client = FrostClient()
    client.connect()

    client.login(
        input('ID: '),
        input('Username: '),
        input('Password: ')
    )
    msgs = client.get_all_msgs()
    messages.contents = msgs
    print(msgs)

    listen(client)
    send_msg(client)

    # client.close()
