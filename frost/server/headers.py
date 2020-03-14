from enum import Enum


class Header(Enum):
    """The header enums.
    """
    METHOD: int = 0
    AUTH_TOKEN: int = 1
    ID_TOKEN: int = 2
    STATUS: int = 3


class Method(Enum):
    """The method enums.
    """
    LOGIN: int = 0
    REGISTER: int = 1
    POST_REGISTER: int = 2

    SEND_MSG: int = 3

    NEW_MSG: int = 4
    GET_NEW_MSG: int = 5

    ALL_MSG: int = 6
    GET_ALL_MSG: int = 7

    NEW_TOKEN: int = 8
    NEW_ID: int = 9


class Status(Enum):
    """The status enums
    """
    SUCCESS: int = 0

    INVALID_AUTH: int = 1
    DUPLICATE_USERNAME: int = 2
