from enum import Enum


class Header(Enum):
    METHOD: int = 0
    AUTH_TOKEN: int = 1
    ID_TOKEN: int = 2


class Method(Enum):
    LOGIN: int = 0
    REGISTER: int = 1
    
    SEND_MSG: int = 2
    NEW_MSG: int = 3
    GET_ALL_MSG: int = 4
    ALL_MSG: int = 5
    
    NEW_TOKEN: int = 6
    NEW_ID: int = 7
