import secrets
from datetime import datetime
from typing import Any, Dict, Union

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from frost.ext import Cog
from frost.server.auth import auth_required
from frost.server.headers import Status
from frost.server.logger import logger
from frost.server.storage import Base, DuplicateValueError, Message, User


class Auth(Cog, route='authentication'):
    """Deals with user authentication. :code:`route='authentication'`
    """

    def register(data: Dict[str, Any], **kwargs: Any) -> None:
        """Registers the a new user with the given data.

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
                f'User "{username}" tried to register for an already existing username'
            )
            kwargs['client_send']({
                'headers': {
                    'path': 'authentication/post_register',
                    'status': Status.DUPLICATE_USERNAME.value
                }
            })

        else:
            logger.info(f'New user registered: {username}')
            kwargs['client_send']({
                'headers': {
                    'path': 'authentication/post_register',
                    'status': Status.SUCCESS.value
                }
            })

    def login(data: Dict[str, Any], **kwargs: Any) -> None:
        """Logs in the given user with the given data.

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
                Base.commit(contents)

                kwargs['client_send']({
                    'headers': {
                        'path': 'authentication/post_login',
                        'status': Status.SUCCESS.value
                    },
                    'token': token,
                    'id': id_
                })
                logger.info(f'User "{username}" logged in')

                Msgs._get_all_msgs(data, token, id_, **kwargs)

                logger.info(f'Sent user "{username}" all messages')
                return

        kwargs['client_send']({
            'headers': {
                'path': 'authentication/post_login',
                'status': Status.INVALID_AUTH.value
            }
        })
        logger.info(f'User tried to log in with username: {username}')


class Msgs(Cog, route='messages'):
    """Deals with user messages. :code:`route='messages'`
    """

    @auth_required
    def send_msg(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        """Saves and stores the message received from a client.

        :param data: Data received from a client
        :type data: Dict[str, Any]
        :param token: The user's token, autofilled by :meth:`frost.server.auth.auth_required`
        :type token: str
        :param id_: The user's ID, autofilled by :meth:`frost.server.auth.auth_required`
        :type id_: str
        """
        msg = data['msg']

        if msg:
            user = User.search(id_)
            username = user['username']
            timestamp = str(datetime.now())

            msg_id = Message.add(
                Message(msg, timestamp, {
                    'username': username,
                    'id': id_
                })
            )

            send = kwargs['send']
            conns = kwargs['users'].values()

            for conn in conns:
                send(conn, {
                    'headers': {
                        'path': 'messages/new'
                    },
                    'msg': {
                        msg_id: Message.search(msg_id)
                    }
                })

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
        data: Dict[str, Any],
        token: str,
        id_: str,
        max_: int = 100,
        **kwargs: Any
    ) -> None:
        """Gets up to :code:`max_` past messages.

        :param data: Data received from the client
        :type data: Dict[str, Any]
        :param max_: The maximum number of messages to get, defaults to 50
        :type max_: int, optional
        :param token: The user's token, autofilled by :meth:`frost.server.auth.auth_required`
        :type token: str
        :param id_: The user's ID, autofilled by :meth:`frost.server.auth.auth_required`
        :type id_: str
        """
        Msgs._get_all_msgs(data, token, id_, max_, **kwargs)

    def _get_all_msgs(
        data: Dict[str, Any],
        token: str,
        id_: str,
        max_: int = 100,
        **kwargs: Any
    ) -> None:
        """Gets up to :code:`max_` past messages.

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

            if msg_id != 'meta' and idx > max_:
                break

        kwargs['client_send']({
            'headers': {
                'path': 'messages/new'
            },
            'msg': Msgs._sort_msgs(result)
        })
