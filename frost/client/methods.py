from typing import Any, Callable, Dict, Union
import json

from .headers import Header, Method


def _store_data(name, data):
    value = data[name]

    with open('.frost', 'r') as f:
        contents = json.load(f)

    contents[name] = value

    with open('.frost', 'w') as f:
        json.dump(contents, f, indent=2)

    return value


def _store_token(data):
    return _store_data('auth_token', data)


def _store_id(data):
    return _store_data('id', data)


def _all_msgs(data):
    return data['msgs']


METHODS: Dict[Union[Header, Method], Callable] = {
    Method.NEW_TOKEN.value: _store_token,
    Method.NEW_ID.value: _store_id,
    Method.ALL_MSG.value: _all_msgs
}


def exec_method(item, data) -> Any:
    return METHODS[item](data)
