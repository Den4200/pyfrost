from frost.server import (
    FrostServer,
    Room
)


app = FrostServer(__file__)


@app.room('/general')
def general(room: 'Room'):
    return room.clients


def run():
    # print(general())
    app.run()
