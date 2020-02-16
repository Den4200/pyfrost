import time
from frost import FrostClient
from frost.client import Header, Method


def run_client():
    with FrostClient() as client:
        client.send({
            'headers': {
                Header.METHOD.value: Method.LOGIN.value
            },
            'username': 'user1',
            'password': 'password'
        })
        client.recieve()
