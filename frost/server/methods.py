from typing import Any, Callable, Dict, Optional, Union
from datetime import datetime
from enum import Enum  # NOQA: F401
import secrets

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from frost.server.ext import Cog
from frost.server.logger import logger
from frost.server.auth import auth_required
from frost.server.headers import Header, Method, Status
from frost.server.storage import (
    Base,
    User,
    Message,
    DuplicateValueError
)


class Auth(Cog, route='authentication'):

    def register(self, send: Callable, data: Dict[str, Any]) -> Union[str, 'Status']:
        """Registers the a new user with the given data.

        :param data: Data received from the client
        :type data: Dict[str, Any]
        :return: The newly created user's ID
        :rtype: str
        """
        username = data['username']
        password = generate_password_hash(
            data['password']
        )

        try:
            User.add(
                User(
                    username=username,
                    password=password
                )
            )

        except DuplicateValueError:
            logger.debug(
                f'User tried to register for an already existing username: {username}'
            )
            send({
                'headers': {
                    Header.METHOD.value: Method.POST_REGISTER.value,
                    Header.STATUS.value: Status.DUPLICATE_USERNAME.value
                }
            })

        else:
            logger.info(f'New user registered: {username}')
            send({
                'headers': {
                    Header.METHOD.value: Method.POST_REGISTER.value,
                    Header.STATUS.value: Status.SUCCESS.value
                }
            })

    def login(self, send: Callable, data: Dict[str, Any]) -> Dict[str, 'Enum']:
        """Logs in the given user with the given data.

        :param data: Data received from the client
        :type data: Dict[str, Any]
        :return: The user's ID, newly generated token, and status OR just the status
        :rtype: Dict[str, 'Enum']
        """
        username = data['username']
        password = data['password']

        users = User.entries()
        contents = Base.data()

        for id_, user in users.items():
            if (
                id_ != 'meta' and
                user['username'] == username and
                check_password_hash(user['password'], password)
            ):
                token = secrets.token_urlsafe()
                contents['users'][id_]['token'] = token

                logger.info(f'User logged in: {username}')

                Base.commit(contents)
                return send({
                    'headers': {
                        Header.METHOD.value: Method.NEW_TOKEN.value,
                        Header.STATUS.value: Status.SUCCESS.value
                    },
                    'auth_token': token,
                    'id': id_
                })

        return send({
            'headers': {
                Header.METHOD.value: Method.NEW_TOKEN.value,
                Header.STATUS.value: Status.INVALID_AUTH.value
            }
        })


class Msgs(Cog, route='messages'):

    @auth_required
    def send_msg(self, send: Callable, data: Dict[str, Any], token=None, id_=None):
        """Saves and stores the message received from a client.

        :param data: Data received from a client
        :type data: Dict[str, Any]
        :param token: The user's token, autofilled by :meth:`frost.server.auth.auth_required`
        :type token: str, optional
        :param id_: The user's ID, autofilled by :meth:`frost.server.auth.auth_required`
        :type id_: str, optional
        """
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

        logger.info(f'[ Message ] {username}: {msg}')

    def _sort_msgs(
        self, send: Callable, msgs: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
    ) -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
        """Sorts messages ascending by ID number.

        :param msgs: The messages to be sorted
        :type msgs: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
        :return: The sorted messages
        :rtype: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
        """
        sorted_ids = sorted([
            int(id_) for id_ in msgs if id_ != 'meta'
        ])
        return {str(id_): msgs[str(id_)] for id_ in sorted_ids}

    @auth_required
    def get_all_msgs(
        self,
        send: Callable,
        data: Dict[str, Any],
        max_: int = 50,
        token: str = None,
        id_: str = None
    ) -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
        """Gets up to :code:`max_` past messages.

        :param data: Data received from the client
        :type data: Dict[str, Any]
        :param max_: The maximum number of messages to get, defaults to 50
        :type max_: int, optional
        :param token: The user's token, autofilled by :meth:`frost.server.auth.auth_required`
        :type token: str, optional
        :param id_: The user's ID, autofilled by :meth:`frost.server.auth.auth_required`
        :type id_: str, optional
        :return: Past messages
        :rtype: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
        """
        msgs = Message.entries()
        rev_entries = reversed(list(msgs))
        result = dict()

        for idx, msg_id in enumerate(rev_entries, 1):
            result[msg_id] = msgs[msg_id]

            if msg_id != 'meta' and idx >= max_:
                break

        logger.info(f'User ID: {id_} requested {len(result) - 1} messages')
        send({
            'headers': {
                Header.METHOD.value: Method.ALL_MSG.value
            },
            'msgs': self._sort_msgs(result)
        })

    @auth_required
    def get_new_msgs(
        self,
        send: Callable,
        data: Dict[str, Any],
        token: str = None,
        id_: str = None
    ) -> Optional[Dict[str, Dict[str, Union[str, Dict[str, str]]]]]:
        """Gets all new messages for a client.

        :param data: Data received from the client
        :type data: Dict[str, Any]
        :param token: The user's token, autofilled by :meth:`frost.server.auth.auth_required`
        :type token: str, optional
        :param id_: The user's ID, autofilled by :meth:`frost.server.auth.auth_required`
        :type id_: str, optional
        :return: New messages
        :rtype: Optional[Dict[str, Dict[str, Union[str, Dict[str, str]]]]]
        """
        last_ts = data.get('last_msg_timestamp')

        if last_ts is None:
            return self._get_all_msgs(data)

        msgs = Message.entries()
        rev_entries = reversed(list(msgs.items()))
        contents = {'headers': {Header.METHOD.value: Method.NEW_MSG.value}}

        last_ts = datetime.strptime(last_ts, r'%Y-%m-%d %H:%M:%S.%f')
        results = dict()

        for msg_id, msg in rev_entries:
            if msg_id == 'meta':
                continue

            msg_ts = datetime.strptime(
                msg['timestamp'],
                r'%Y-%m-%d %H:%M:%S.%f'
            )

            if msg_ts > last_ts:
                results[msg_id] = msg
            else:
                break

        if len(results) > 0:
            logger.info(f'User ID: {id_} requested {len(results)} messages')
            contents['msgs'] = self._sort_msgs(results)

        send(contents)

# METHODS: Dict[int, Callable] = {
#     Method.REGISTER.value: _register,
#     Method.LOGIN.value: _login,
#     Method.SEND_MSG.value: _send_msg,
#     Method.GET_ALL_MSG.value: _get_all_msgs,
#     Method.GET_NEW_MSG.value: _get_new_msgs
# }


# def exec_method(item: Any, data: Dict[Any, Any]) -> Any:
#     """Executes the method specified in the :code:`data` headers.

#     :param item: The specific method to execute
#     :type item: Any
#     :param data: Data received from the server
#     :type data: Dict[Any, Any]
#     :return: The data the specific method returned
#     :rtype: Any
#     """
#     return METHODS[item](data)

Auth()
Msgs()
