from frost import FrostClient


def run_client():
    with FrostClient() as client:
        # client.login('1', 'user1', 'password')

        # client.send_msg('testing 123')
        # time.sleep(2)
        # client.send_msg('you good?')

        client.get_all_msgs()
