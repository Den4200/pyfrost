import time

from frost import FrostClient
from frost.client import Status, threaded
from frost.client.events import Messages, EventStatus, Memory


@threaded(daemon=True)
def check_msgs() -> None:
    while True:
        msgs = Messages.get_new_msgs()

        if msgs:
            print(Messages.all)

        time.sleep(0.25)


@threaded()
def send_msg(client: 'FrostClient'):
    while True:
        msg = input()
        client.send_msg(1, msg)


def get_status(name):
    status = None
    while status is None:
        status = EventStatus.get_status(name)

    return status


def create_room(client: 'FrostClient', name: str):
    client.create_room(name)
    print(get_status('create_room'))


def get_invite_code(client: 'FrostClient', room_id: int):
    client.get_invite_code(room_id)
    status = get_status('get_invite_code')

    if status == Status.SUCCESS.value:
        print(Memory.rooms[room_id].invite_code)
        print(status)
    else:
        print(f'get_invite_code failed. code: {status}')


def get_joined_rooms(client: 'FrostClient'):
    client.get_joined_rooms()
    status = get_status('get_joined_rooms')

    if status == Status.SUCCESS.value:
        print(Memory.rooms)
        print(status)
    else:
        print(f'get_joined_rooms failed. code: {status}')


def join_room(client: 'FrostClient', invite_code: str):
    client.join_room(invite_code)
    print(get_status('join_room'))


def leave_room(client: 'FrostClient', room_id: int):
    client.leave_room(room_id)
    print(get_status('leave_room'))


def get_room_msgs(client: 'FrostClient', room_id: int):
    client.get_room_msgs(room_id)
    print(get_status('get_room_msgs'))


def get_room_members(client: 'FrostClient', room_id: int):
    client.get_room_members(room_id)
    status = get_status('get_room_members')

    if status == Status.SUCCESS.value:
        print(Memory.rooms[room_id].members)
        print(status)
    else:
        print(f'get_room_members failed. code: {status}')


def run_client():
    client = FrostClient()
    client.connect()

    # reg = None
    # while reg in (Status.INVALID_AUTH.value, None):
    #     client.login(
    #         input('Username: '),
    #         input('Password: ')
    #     )
    #     reg = get_status('register')

    login = None
    while login in (Status.INVALID_AUTH.value, None):
        client.login(
            input('Username: '),
            input('Password: ')
        )
        login = get_status('login')

    get_joined_rooms(client)

    join_room(client, 'aff10152-6d4c-11ea-87fe-9cb6d0d6fdc2')
    print(Memory.rooms)

    get_room_msgs(client, 2)
    time.sleep(0.25)
    print(Messages.all[2])

    get_room_members(client, 2)

    leave_room(client, 2)
    print(Memory.rooms)

    # send_msg(client)
    # check_msgs()

    client.close()
