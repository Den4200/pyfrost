import socket
from typing import Dict, Tuple, Union

from .exceptions import MaxRoomSize


class Room:

    def __init__(self, size: int = 25) -> None:
        if size > 25:
            raise MaxRoomSize(
                'The maximum room size has been surpassed.'
            )
        self.size = size
        self.clients = dict()

    # TODO: add_client
    # TODO: pop_client

