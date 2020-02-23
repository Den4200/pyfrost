import time
from frost import FrostClient


def run_client():
    with FrostClient() as client:
        # client.login('1', 'user1', 'password')

        # client.send_msg('hello, world!')
        # time.sleep(2)
        # client.send_msg('testing testing 123')

        client.get_all_msgs()

