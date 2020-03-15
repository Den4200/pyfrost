from typing import Any, Callable, Dict, Union
from datetime import datetime
from enum import Enum  # NOQA: F401
import secrets

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from frost.ext import Cog
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
    """Deals with user authentication. :code:`route='authentication'`
    """

    def register(send: Callable, data: Dict[str, Any]) -> None:
        """Registers the a new user with the given data.

        :param send: The function to send data back to the client
        :type send: Callable
        :param data: Data received from the client
        :type data: Dict[str, Any]
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
            logger.info(
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

    def login(send: Callable, data: Dict[str, Any]) -> None:
        """Logs in the given user with the given data.

        :param send: The function to send data back to the client
        :type send: Callable
        :param data: Data received from the client
        :type data: Dict[str, Any]
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
                send({
                    'headers': {
                        Header.METHOD.value: Method.NEW_TOKEN.value,
                        Header.STATUS.value: Status.SUCCESS.value
                    },
                    'auth_token': token,
                    'id': id_
                })
                return

        send({
            'headers': {
                Header.METHOD.value: Method.NEW_TOKEN.value,
                Header.STATUS.value: Status.INVALID_AUTH.value
            }
        })


class Msgs(Cog, route='messages'):
    """Deals with user messages. :code:`route='messages'`
    """

    @auth_required
    def send_msg(send: Callable, data: Dict[str, Any], token: str, id_: str) -> None:
        """Saves and stores the message received from a client.

        :param send: The function to send data back to the client
        :type send: Callable
        :param data: Data received from a client
        :type data: Dict[str, Any]
        :param token: The user's token, autofilled by :meth:`frost.server.auth.auth_required`
        :type token: str
        :param id_: The user's ID, autofilled by :meth:`frost.server.auth.auth_required`
        :type id_: str
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
        msgs: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
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
        send: Callable,
        data: Dict[str, Any],
        token: str,
        id_: str,
        max_: int = 250,
    ) -> None:
        """Gets up to :code:`max_` past messages.

        :param send: The function to send data back to the client
        :type send: Callable
        :param data: Data received from the client
        :type data: Dict[str, Any]
        :param max_: The maximum number of messages to get, defaults to 50
        :type max_: int, optional
        :param token: The user's token, autofilled by :meth:`frost.server.auth.auth_required`
        :type token: str
        :param id_: The user's ID, autofilled by :meth:`frost.server.auth.auth_required`
        :type id_: str
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
            'msgs': Msgs._sort_msgs(result)
        })

    @auth_required
    def get_new_msgs(
        send: Callable,
        data: Dict[str, Any],
        token: str,
        id_: str
    ) -> None:
        """Gets all new messages for a client.

        :param send: The function to send data back to the client
        :type send: Callable
        :param data: Data received from the client
        :type data: Dict[str, Any]
        :param token: The user's token, autofilled by :meth:`frost.server.auth.auth_required`
        :type token: str
        :param id_: The user's ID, autofilled by :meth:`frost.server.auth.auth_required`
        :type id_: str
        """
        last_ts = data.get('last_msg_timestamp')

        if last_ts is None:
            return Msgs.get_all_msgs(send, data)

        msgs = Message.entries()
        rev_entries = reversed(list(msgs.items()))
        contents = {
            'headers': {
                Header.METHOD.value: Method.NEW_MSG.value
            },
            'msgs': {}
        }

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
            contents['msgs'] = Msgs._sort_msgs(results)

        send(contents)
