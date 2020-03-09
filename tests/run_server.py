from frost.server import FrostServer


app = FrostServer(__file__)


def run_server():
    app.run()
