from typing import Any, Callable, Dict, Union
import secrets

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from .headers import Header, Method
from .storage import Base, User
from .auth import auth_required


def _register(data) -> None:
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

        Base.commit(contents)
        return token

@auth_required
def _send_msg(data, token=None, id_=None) -> None:
    msg = data['msg']
    user = User.search(id_)
    
    print(f'{user["username"]}: {msg}')
    return id_, msg

METHODS: Dict[int, Callable] = {
    Method.REGISTER.value: _register,
    Method.LOGIN.value: _login,
    Method.SEND_MSG.value: _send_msg
}


def exec_method(item, data) -> Any:
    return METHODS[item](data)
