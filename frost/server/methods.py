from typing import Any, Callable, Dict
from datetime import datetime
import secrets
import logging

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from .headers import Method
from .storage import Base, User, Message
from .auth import auth_required


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

    logging.info(f'New user registered: {username}')
    return id_


def _login(data) -> str:
    id_ = data['id']
    username = data['username']
    password = data['password']

    contents = Base.data()
    user = User.search(id_)

    if (user is not None and
        user['username'] == username and
        check_password_hash(user['password'], password)
        ):
        token = secrets.token_urlsafe()
        contents['users'][id_]['token'] = token

        logging.info(f'User logged in: {username}')

        Base.commit(contents)
        return token


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

    logging.info(f'[ Message ] {username}: {msg}')
    return {
        'from_user': {
            'username': username,
            'id': id_
        },
        'msg': msg,
        'timestamp': timestamp
    }


@auth_required
def _get_all_msgs(data, max_=50, token=None, id_=None):
    msgs = Message.entries()
    result = dict()

    for idx, msg_id in enumerate(msgs):
        if idx >= max_:
            break

        result[msg_id] = msgs[msg_id]

    logging.info(f'User ID: {id_} requested all {msg_id} messages')
    return result
    

METHODS: Dict[int, Callable] = {
    Method.REGISTER.value: _register,
    Method.LOGIN.value: _login,
    Method.SEND_MSG.value: _send_msg,
    Method.GET_ALL_MSG.value: _get_all_msgs
}


def exec_method(item, data) -> Any:
    return METHODS[item](data)
