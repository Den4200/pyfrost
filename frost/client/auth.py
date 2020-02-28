import json
import functools


@functools.lru_cache()
def get_auth_token():
    with open('.frost', 'r') as f:
        return json.load(f)['auth_token']


@functools.lru_cache()
def get_id():
    with open('.frost', 'r') as f:
        return json.load(f)['id']


def get_auth(func):
    """
    A decorator to get the saved
    auth token and id.
    """
    def execute(*args, **kwargs):
        return func(
            *args, **kwargs,
            token=get_auth_token(),
            id_=get_id()
        )
    return execute
