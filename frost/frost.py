from pathlib import Path
from .socketio import Server, threaded


class Frost(Server):
    """
    The Frost server.
    """

    def __init__(self, file: str) -> None:
        super(Frost, self).__init__()
        path = Path(file)

        self._name = path.name
        self._dir = path.parent

    def run(self, ip: str = '127.0.0.1', port: int = 5555) -> None:
        """
        Runs the Frost Server.
        """
        self.ip = ip
        self.port = port
        
        self.start()
