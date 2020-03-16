from enum import Enum


class Status(Enum):
    """The status enums
    """
    SUCCESS: int = 0

    INVALID_AUTH: int = 1
    DUPLICATE_USERNAME: int = 2
