import socket
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    ONLINE:  int = 0
    AFK:     int = 1
    DND:     int = 2
    OFFLINE: int = 3


@dataclass
class User:
    name: str
    status: Optional[Status] = None
    conn: Optional['socket.socket'] = None
    raddr: Optional[Tuple[str, int]] = None
