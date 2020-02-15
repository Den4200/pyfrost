from typing import Any, Callable, Dict, Union
import secrets

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from .headers import Header, Method
from .database import db_session, User


def _register(data) -> None:
    username = data['username']
    password = generate_password_hash(
        data['password']
    )

    new_user = User(
        username=username, 
        password=password,
    )
    db_session.add(new_user)
    db_session.commit()

def _login(data) -> str:
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        token = secrets.token_urlsafe()
        return token


METHODS: Dict[Union[Header, Method], Callable] = {
    Method.REGISTER.value: _register,
    Method.LOGIN.value: _login
}


def exec_method(item, data) -> Any:
    return METHODS[item](data)
