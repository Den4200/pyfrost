from enum import Enum


class Header(Enum):
    METHOD: int = 0
    AUTH_TOKEN: int = 1


class Method(Enum):
    LOGIN: int = 0
    REGISTER: int = 1
    
    SEND_MSG: int = 2
    NEW_MSG: int = 3
    
    NEW_TOKEN: int = 4
