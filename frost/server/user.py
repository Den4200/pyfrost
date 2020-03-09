import socket  # NOQA: F401
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    """The user status enums.
    """
    ONLINE:  int = 0
    AFK:     int = 1
    DND:     int = 2
    OFFLINE: int = 3


@dataclass
class User:
    """Represents a user.

    :raises NotImplementedError: This class is not implemented yet
    """
    name: str

    status: Optional[Status] = None
    afk_timeout: Optional[int] = None

    conn: Optional['socket.socket'] = None
    raddr: Optional[Tuple[str, int]] = None

    def __post_init__(self) -> None:
        raise NotImplementedError

    def check(self) -> None:
        """Does general checks on the user and should be run every tick.
        """
        if self.status not in (None, Status.DND, Status.OFFLINE):

            if self.afk_timeout >= 900:
                self.status = Status.AFK

            elif self.status:
                self.status = Status.ONLINE

        if self.status is not None and not isinstance(self.status, Status):
            raise TypeError(
                'User status only accepts an instance of the Status class'
            )
