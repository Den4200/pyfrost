from typing import Any, Callable, Dict
from datetime import datetime
import secrets

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from .headers import Method
from .storage import Base, User, Message
from .auth import auth_required
from .logger import logger


def _register(data) -> str:
    username = data['username']
    password = generate_password_hash(
        data['password']
    )

    id_ = User.add(
        User(
            username=username,
            password=password
        )
    )

    logger.info(f'New user registered: {username}')
    return id_


def _login(data) -> str:
    username = data['username']
    password = data['password']

    users = User.entries()
    contents = Base.data()

    for id_, user in users.items():
        if (
            id_ != 'meta' and
            user['username'] == username and
            check_password_hash(user['password'], password)
        ):
            token = secrets.token_urlsafe()
            contents['users'][id_]['token'] = token

            logger.info(f'User logged in: {username}')

            Base.commit(contents)
            return {
                'token': token,
                'id': id_
            }


@auth_required
def _send_msg(data, token=None, id_=None):
    msg = data['msg']
    user = User.search(id_)
    username = user['username']
    timestamp = str(datetime.now())

    Message.add(
        Message(msg, timestamp, {
            'username': username,
            'id': id_
        })
    )

    logger.info(f'[ Message ] {username}: {msg}')
    return {
        'from_user': {
            'username': username,
            'id': id_
        },
        'msg': msg,
        'timestamp': timestamp
    }


def _sort_msgs(msgs):
    sorted_ids = sorted([
        int(id_) for id_ in msgs if id_ != 'meta'
    ])
    return {str(id_): msgs[str(id_)] for id_ in sorted_ids}


@auth_required
def _get_all_msgs(data, max_=50, token=None, id_=None):
    msgs = Message.entries()
    rev_entries = reversed(list(msgs))
    result = dict()

    for idx, msg_id in enumerate(rev_entries, 1):
        result[msg_id] = msgs[msg_id]

        if msg_id != 'meta' and idx >= max_:
            break

    logger.info(f'User ID: {id_} requested {len(result) - 1} messages')
    return _sort_msgs(result)


@auth_required
def _get_new_msgs(data, token=None, id_=None):
    last_ts = data.get('last_msg_timestamp')

    if last_ts is None:
        return _get_all_msgs(data)

    msgs = Message.entries()
    rev_entries = reversed(list(msgs.items()))

    last_ts = datetime.strptime(last_ts, r'%Y-%m-%d %H:%M:%S.%f')
    results = dict()

    for msg_id, msg in rev_entries:
        msg_ts = datetime.strptime(
            msg['timestamp'],
            r'%Y-%m-%d %H:%M:%S.%f'
        )

        if msg_ts > last_ts:
            results[msg_id] = msg
        else:
            break

    if len(results) > 0:
        logger.info(f'User ID: {id_} requested {len(results)} messages')
        return _sort_msgs(results)


METHODS: Dict[int, Callable] = {
    Method.REGISTER.value: _register,
    Method.LOGIN.value: _login,
    Method.SEND_MSG.value: _send_msg,
    Method.GET_ALL_MSG.value: _get_all_msgs,
    Method.GET_NEW_MSG.value: _get_new_msgs
}


def exec_method(item, data) -> Any:
    return METHODS[item](data)
