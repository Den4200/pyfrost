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

    SEND_MSG: int = 2

    NEW_MSG: int = 3
    GET_NEW_MSG: int = 4

    ALL_MSG: int = 5
    GET_ALL_MSG: int = 6

    NEW_TOKEN: int = 7
    NEW_ID: int = 8


class Status(Enum):
    """The status enums
    """
    SUCCESS = 0
    INVALID_AUTH = 1
