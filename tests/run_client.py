import time
from frost import FrostClient
from frost.client import Header, Method


def run_client():
    with FrostClient() as client:
        client.send({
            'headers': {
                Header.METHOD.value: Method.REGISTER.value
            },
            'username': 'user2',
            'password': 'password'
        })
        client.recieve()
