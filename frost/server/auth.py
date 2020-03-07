from frost.server.headers import Header
from frost.server.storage import User


def auth_required(func):

    def execute(*args, **kwargs):
        id_ = args[0]['headers'].get(Header.ID_TOKEN.value)
        token = args[0]['headers'].get(Header.AUTH_TOKEN.value)

        if id_ is not None and token is not None:
            user = User.search(id_)

            if user is not None and user['token'] == token:
                return func(*args, **kwargs, id_=id_, token=token)

    return execute
