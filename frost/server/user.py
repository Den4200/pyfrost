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
    afk_timeout: Optional[int] = None

    conn: Optional['socket.socket'] = None
    raddr: Optional[Tuple[str, int]] = None

    def check(self) -> None:
        """
        Does general checks on the user
        and should be run every.

        Checks user's status and makes sure
        self.status is an instance of Status.
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
