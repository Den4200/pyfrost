import time

from frost import FrostClient
from frost.client import Status, threaded  # NOQA: F401
from frost.client.events import messages, login_status, register_status  # NOQA: F401


@threaded(daemon=True)
def check_msgs() -> None:
    while True:
        msgs = messages.get_new_msgs()

        if msgs:
            print(messages.all_messages)

        time.sleep(0.25)


@threaded()
def send_msg(client: 'FrostClient'):
    while True:
        msg = input()
        client.send_msg(msg)


def run_client():
    client = FrostClient()
    client.connect()

    # reg = None
    # while reg in (Status.INVALID_AUTH.value, None):
    #     client.login(
    #         input('Username: '),
    #         input('Password: ')
    #     )
    #     status = None
    #     while status is None:
    #         reg = status = register_status.get_status()
    #         time.sleep(0.1)

    login = None
    while login in (Status.INVALID_AUTH.value, None):
        client.login(
            input('Username: '),
            input('Password: ')
        )
        status = None
        while status is None:
            login = status = login_status.get_status()
            time.sleep(0.1)

    send_msg(client)
    check_msgs()

    # client.get_all_msgs()
    # client.close()
