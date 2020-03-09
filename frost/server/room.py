from frost.server.exceptions import MaxRoomSize


class Room:
    """A virtual room within the server to separate clients.

    :raises NotImplementedError: This class is not implemented yet
    """

    def __init__(self, path, size: int = 25) -> None:
        raise NotImplementedError

        if size > 25:
            raise MaxRoomSize(
                'The maximum room size has been surpassed.'
            )
        self._size = size
        self._path = path
        self.clients = dict()

    # TODO: add_client
    # TODO: pop_client
