from frost import FrostClient


def run_client():
    client = FrostClient(__file__)
    
    client.send({
        'username': 'bobby',
        'password': 'super-secret-password'
    })
    client.close()
