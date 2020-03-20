import secrets
from typing import Any, Dict, Union

from sqlalchemy.exc import IntegrityError
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from frost.ext import Cog
from frost.server.auth import auth_required
from frost.server.database import managed_session, Message, Room, User
from frost.server.headers import Status
from frost.server.logger import logger


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
            with managed_session() as session:
                user = User(
                    username=username,
                    password=password
                )
                user.joined_rooms.append(
                    session.query(Room).first()
                )
                session.add(user)

        except IntegrityError:
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

        with managed_session() as session:
            user = session.query(User).filter(User.username == username).first()

            if user is not None and check_password_hash(user.password, password):
                user.token = secrets.token_urlsafe()

                kwargs['client_send']({
                    'headers': {
                        'path': 'authentication/post_login',
                        'status': Status.SUCCESS.value
                    },
                    'token': user.token,
                    'id': user.id
                })
                logger.info(f'User "{username}" logged in')

                Msgs._get_all_msgs(data, user.token, user.id, **kwargs)

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
        raw_msg = data['msg']
        send = kwargs['send']
        conns = kwargs['users'].values()

        if raw_msg:
            with managed_session() as session:
                user = session.query(User).filter(User.id == id_).first()
                msg = Message(
                    message=raw_msg,
                    user_id=user.id,
                    room_id=1  # room_id is hardcoded until separate rooms are implemeneted
                )
                session.add(msg)

                contents = {
                    'headers': {
                        'path': 'messages/new'
                    },
                    'msg': {
                        msg.id: {
                            'message': raw_msg,
                            'from_user': {
                                'username': user.username,
                                'id': user.id
                            },
                            'timestamp': msg.timestamp
                        }
                    }
                }
                logger.info(f'[ Message ] {user.username}: {raw_msg}')

            for conn in conns:
                send(conn, contents)

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
        with managed_session() as session:
            msgs = session.query(Message).limit(max_)

            msgs = {
                msg.id: {
                    'message': msg.message,
                    'from_user': {
                        'username': msg.user.username,
                        'id': msg.user_id
                    },
                    'timestamp': str(msg.timestamp)
                } for msg in msgs
            }

        kwargs['client_send']({
            'headers': {
                'path': 'messages/new'
            },
            'msg': msgs
        })
