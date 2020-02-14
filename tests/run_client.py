import time
from frost import FrostClient


def run_client():
    with FrostClient() as client:
        client.send({
            'username': 'bobby',
            'password': 'super-secret-password'
        })
        time.sleep(5)
        client.send({
            'username': 'joe',
            'password': 'another-super-secret-password'
        })
