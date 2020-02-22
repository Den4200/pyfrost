import time
from frost import FrostClient


def run_client():
    with FrostClient() as client:
        # client.login('1', 'user1', 'password')

        client.send_msg('hello, world!')
        client.send_msg('testing testing 123')
