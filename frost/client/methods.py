from typing import Any, Callable, Dict, Union
from functools import partial

from .headers import Header, Method


def _store_token(data) -> None:
    token = data['auth_token']

    with open('token.key', 'w') as f:
        f.write(token)

    return token


METHODS: Dict[Union[Header, Method], Callable] = {
    Method.NEW_TOKEN.value: _store_token,
}


def exec_method(item, data) -> Any:
    return METHODS[item](data)
