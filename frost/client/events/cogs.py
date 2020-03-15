from typing import Any, Dict
import json

from frost.ext import Cog
from frost.client.headers import Status
from frost.client.events.events import messages


class Auth(Cog, route='authentication'):

    def post_register(data: Dict[str, Any]) -> None:

        return data['headers']['status']

    def post_login(data: Dict[str, Any]) -> None:
        return Auth._store_token(data)

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
        if data['headers']['status'] == Status.SUCCESS.value:
            Auth._store_data('auth_token', data)
            Auth._store_id(data)
            return Status.SUCCESS.value

        return Status.INVALID_AUTH.value

    def _store_id(data: Dict[Any, Any]) -> str:
        """Stores the ID from :code:`data` in :code:`.frost`.

        :param data: Data received from the server
        :type data: Dict[Any, Any]
        :return: The ID
        :rtype: str
        """
        return Auth._store_data('id', data)


class Msgs(Cog, route='messages'):

    def new(data: Dict[str, Any]) -> None:
        messages.new_messages.update(data['msg'])
