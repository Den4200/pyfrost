from typing import Any, Callable, Dict, Union
import json

from frost.client.headers import Header, Method, Status


def _store_data(key: str, data: Dict[Any, Any]) -> Any:
    """Stores data into the :code:`.frost` file.

    :param key: The key of where to find the data to store
    :type key: str
    :param data: Data received from the server
    :type data: Dict[Any, Any]
    :return: The value of the key in `data`
    :rtype: Any
    """
    value = data[key]

    with open('.frost', 'r') as f:
        contents = json.load(f)

    contents[key] = value

    with open('.frost', 'w') as f:
        json.dump(contents, f, indent=2)

    return value


def _store_token(data: Dict[Any, Any]) -> int:
    """Stores the auth token and ID from :code:`data` in :code:`.frost`.

    :param data: Data received from the server
    :type data: Dict[Any, Any]
    :return: The status code received from the server
    :rtype: int
    """
    if data['headers'][Header.STATUS.value] == Status.SUCCESS.value:
        _store_data('auth_token', data)
        _store_id(data)
        return Status.SUCCESS.value

    return Status.INVALID_AUTH.value


def _store_id(data: Dict[Any, Any]) -> str:
    """Stores the ID from :code:`data` in :code:`.frost`.

    :param data: Data received from the server
    :type data: Dict[Any, Any]
    :return: The ID
    :rtype: str
    """
    return _store_data('id', data)


def _update_last_msg_ts(ts: str) -> None:
    """Updates the timestamp for the last message received.

    :param ts: The timestamp for the last message recieved
    :type ts: str
    """
    with open('.frost', 'r') as f:
        contents = json.load(f)

    contents['last_msg_timestamp'] = ts

    with open('.frost', 'w') as f:
        json.dump(contents, f, indent=2)


def _all_msgs(data: Dict[Any, Any]) -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
    """Gets messages from :code:`data` and updates the timestamp for the last received message.

    :param data: Data received from the server
    :type data: Dict[Any, Any]
    :return: The messages received from the server
    :rtype: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
    """
    msgs = data['msgs']

    if msgs:
        _update_last_msg_ts(
            list(msgs.values())[-1]['timestamp']
        )

    return msgs


METHODS: Dict[int, Callable] = {
    Method.NEW_TOKEN.value: _store_token,
    Method.NEW_ID.value: _store_id,
    Method.ALL_MSG.value: _all_msgs,
    Method.NEW_MSG.value: _all_msgs
}


def exec_method(item: Any, data: Dict[Any, Any]) -> Any:
    """Executes the method specified in the :code:`data` headers.

    :param item: The specific method to execute
    :type item: Any
    :param data: Data received from the server
    :type data: Dict[Any, Any]
    :return: The data the specific method returned
    :rtype: Any
    """
    return METHODS[item](data)
