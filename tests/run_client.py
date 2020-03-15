from dataclasses import dataclass

from frost import FrostClient
from frost.client import Status, threaded
from frost.client.events import messages


@threaded(daemon=True)
def listen(client: 'FrostClient') -> None:
    while True:
        msgs = messages.get_new_msgs()

        if msgs:
            print(msgs)


@threaded()
def send_msg(client: 'FrostClient'):
    while True:
        msg = input()
        client.send_msg(msg)


def run_client():
    # with FrostClient() as client:
    client = FrostClient()
    client.connect()

    # reg = None
    # while reg in (Status.DUPLICATE_USERNAME.value, None):
    #     reg = client.register(
    #         input('Register Username: '),
    #         input('Register Password: ')
    #     )

    login = None
    while login in (Status.INVALID_AUTH.value, None):
        login = client.login(
            input('Username: '),
            input('Password: ')
        )

    msgs = client.get_all_msgs()
    messages.contents = msgs
    print(msgs)

    listen(client)
    send_msg(client)

    # client.close()
