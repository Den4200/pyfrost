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

    def post_register(data: Dict[str, Any]) -> None:
        register_status.current_status = data['headers']['status']

    def post_login(data: Dict[str, Any]) -> None:
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

    def new(data: Dict[str, Any]) -> None:
        messages.add_new_msgs(data['msg'])
