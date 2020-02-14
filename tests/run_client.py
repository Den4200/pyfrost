import time
from frost import FrostClient


def run_client():
    with FrostClient() as client:
        client.send({
            'headers': {},
            'username': 'bobby',
            'password': 'super-secret-password'
        })
        client.recieve()
