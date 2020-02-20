from typing import Any, Callable, Dict, Union
import secrets

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from .headers import Header, Method
from .storage import Base, User


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


METHODS: Dict[int, Callable] = {
    Method.REGISTER.value: _register,
    Method.LOGIN.value: _login
}


def exec_method(item, data) -> Any:
    return METHODS[item](data)
