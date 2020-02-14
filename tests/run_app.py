from frost import (
    Frost,
    Room
)


app = Frost(__file__)


@app.room('/general')
def general(room: 'Room'):
    return room.clients


def run():
    print(general())
