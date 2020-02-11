from sys import path
from os.path import dirname

path.append(dirname(path[0]))
__package__ = 'tests'

# ----- #

from frost import Frost

app = Frost(__file__)

app.run()
