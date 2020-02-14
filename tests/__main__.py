from sys import argv
from .run_server import run_server
from .run_client import run_client
# from frost.server.database import init_db

if __name__ == "__main__":
    # init_db()
    if len(argv) == 2:

        if argv[1] == 'server':
            run_server()

        elif argv[1] == 'client':
            run_client()

        else:
            print('Usage: python -m tests <server or client>')

    else:    
        print('Usage: python -m tests <server or client>')
