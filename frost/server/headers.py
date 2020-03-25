from enum import Enum


class Status(Enum):
    """The status enums
    """
    SUCCESS: int = 0

    INVALID_AUTH: int = 1
    PERMISSION_DENIED: int = 2

    DUPLICATE_USERNAME: int = 3

    ROOM_NOT_FOUND: int = 4
    EMPTY_ROOM_NAME: int = 5
    DUPLICATE_ROOM_NAME: int = 6
    INVALID_INVITE: int = 7
