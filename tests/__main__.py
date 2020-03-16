import sys  # NOQA: F401
from sys import argv


def main():
    if len(argv) == 2:

        if argv[1] == 'server':
            from tests.run_server import run_server
            run_server()

        elif argv[1] == 'client':
            from tests.run_client import run_client
            run_client()

        elif argv[1] == 'init_db':
            from frost.server.database import init_db
            init_db()

        else:
            print('Usage: python -m tests <server / client / init_db>')

    else:
        print('Usage: python -m tests <server / client / init_db>')


if __name__ == "__main__":
    main()
