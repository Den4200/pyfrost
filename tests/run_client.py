import time
from frost import FrostClient
from frost.client import Header, Method


def run_client():
    with FrostClient() as client:
        client.send({
            'headers': {
                Header.METHOD.value: Method.LOGIN.value
            },
            'id': '2',
            'username': 'user2',
            'password': 'password'
        })
        client.recieve()
