from typing import Any, Dict
import json

from frost.ext import Cog
from frost.client.headers import Status
from frost.client.events.events import (
    messages,
    login_status,
    register_status
)


class Auth(Cog, route='authentication'):
    """Deals with user authentication. :code:`route='authentication'`
    """

    def post_register(data: Dict[str, Any]) -> None:
        """Deals with the response received from the server after a registration attempt.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        register_status.current_status = data['headers']['status']

    def post_login(data: Dict[str, Any]) -> None:
        """Deals with the response received from the server after a login attempt.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        status = data['headers']['status']

        if status == Status.SUCCESS.value:
            with open('.frost', 'r') as f:
                contents = json.load(f)

            contents.update({
                'id': data['id'],
                'token': data['token']
            })

            with open('.frost', 'w') as f:
                json.dump(contents, f, indent=2)

        login_status.current_status = status


class Msgs(Cog, route='messages'):
    """Deals with user messages. :code:`route='messages'`
    """

    def new(data: Dict[str, Any]) -> None:
        """Deals with new user messages and stores them in :class:`frost.client.events.events.Messages`.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        messages.add_new_msgs(data['msg'])
