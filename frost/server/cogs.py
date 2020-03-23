import secrets
from typing import Any, Dict
import uuid

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
                    session.query(Room).first()  # Auto join main room
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

                # Send the main room messages
                data['room_id'] = 1
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
        room_id = data['room_id']
        send = kwargs['send']
        conns = kwargs['users'].values()

        if raw_msg:
            with managed_session() as session:
                user = session.query(User).filter(User.id == id_).first()
                room = session.query(Room).filter(Room.id == room_id).first()

                msg = Message(
                    message=raw_msg,
                    user_id=user.id,
                    room_id=room_id
                )
                session.add(msg)

                contents = {
                    'headers': {
                        'path': 'messages/new'
                    },
                    'msg': {
                        msg.id: {
                            'message': raw_msg,
                            'room': {
                                'name': room.name,
                                'id': room_id
                            },
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
        room_id = data['room_id']

        with managed_session() as session:
            room = session.query(Room).filter(Room.id == room_id).first()

            if room is None:
                kwargs['client_send']({
                    'headers': {
                        'path': 'messages/post_get_all',
                        'status': Status.ROOM_NOT_FOUND.value
                    }
                })
                return

            msgs = room.messages
            msgs = {
                msg.id: {
                    'message': msg.message,
                    'room': {
                        'name': room.name,
                        'id': room_id
                    },
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


class Rooms(Cog, route='rooms'):

    @auth_required
    def create(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        room_name = data['room_name']

        if not room_name:
            kwargs['client_send']({
                'headers': {
                    'path': 'rooms/post_create',
                    'status': Status.EMPTY_ROOM_NAME.value
                }
            })
            return

        with managed_session() as session:
            room = Room(
                name=room_name,
                owner_id=id_,
                invite_code=str(uuid.uuid1())
            )
            session.add(room)
            user = session.query(User).filter(User.id == id_).first()
            user.joined_rooms.append(room)

            kwargs['client_send']({
                'headers': {
                    'path': 'rooms/post_create',
                    'status': Status.SUCCESS.value
                }
            })
            logger.info(f'User {user.username} created room {room_name}')

    @auth_required
    def join(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        code = data['invite_code']

        with managed_session() as session:
            room = session.query(Room).filter(Room.invite_code == code).first()

            if room is None:
                kwargs['client_send']({
                    'headers': {
                        'path': 'rooms/post_join',
                        'status': Status.INVALID_INVITE.value
                    }
                })
                return

            user = session.query(User).filter(User.id == id_).first()
            user.joined_rooms.append(room)

            kwargs['client_send']({
                'headers': {
                    'path': 'rooms/post_join',
                    'status': Status.SUCCESS.value
                }
            })
            logger.info(f'User {user.username} joined room {room.name}')

    @auth_required
    def leave(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        room_id = data['room_id']

        with managed_session() as session:
            room = session.query(Room).filter(Room.id == room_id).first()

            if room is None:
                kwargs['client_send']({
                    'headers': {
                        'path': 'rooms/post_leave',
                        'status': Status.ROOM_NOT_FOUND.value
                    }
                })
                return

            user = session.query(User).filter(User.id == id_).first()
            user.joined_rooms.remove(room)

            kwargs['client_send']({
                'headers': {
                    'path': 'rooms/post_leave',
                    'status': Status.SUCCESS.value
                }
            })
            logger.info(f'User {user.username} left room {room.name}')

    @auth_required
    def get_invite_code(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        room_id = data['room_id']

        with managed_session() as session:
            room = session.query(Room).filter(Room.id == room_id).first()

            if room is None:
                kwargs['client_send']({
                    'headers': {
                        'path': 'rooms/post_invite_code',
                        'status': Status.ROOM_NOT_FOUND.value
                    }
                })
                return

            if room.owner_id != id_:
                kwargs['client_send']({
                    'headers': {
                        'path': 'rooms/post_invite_code',
                        'status': Status.PERMISSION_DENIED.value
                    }
                })
                return

            kwargs['client_send']({
                'headers': {
                    'path': 'rooms/post_invite_code',
                    'status': Status.SUCCESS.value
                },
                'room_invite_code': room.invite_code
            })

            user = session.query(User).filter(User.id == id_).first()
            logger.info(f"User {user.username} was sent room {room.name}'s invite code'")

    @auth_required
    def get_all_joined(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        with managed_session() as session:
            user = session.query(User).filter(User.id == id_).first()

            rooms = user.joined_rooms
            rooms = [
                {
                    'id': room.id,
                    'name': room.name
                } for room in rooms
            ]

        kwargs['client_send']({
            'headers': {
                'path': 'rooms/post_all_joined',
                'status': Status.SUCCESS.value
            },
            'rooms': rooms
        })

    @auth_required
    def get_members(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        room_id = data['room_id']

        with managed_session() as session:
            room = session.query(Room).filter(Room.id == room_id).first()
            members = room.members

            user = session.query(User).filter(User.id == id_).first()

            if user not in members:
                kwargs['client_send']({
                    'headers': {
                        'path': 'rooms/post_members',
                        'status': Status.PERMISSION_DENIED.value
                    }
                })
                return

            members = [
                {
                    'username': member.username,
                    'id': member.id
                } for member in members
            ]

        kwargs['client_send']({
            'headers': {
                'path': 'rooms/post_members',
                'status': Status.SUCCESS.value
            },
            'members': members
        })
