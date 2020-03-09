"""The logger for the server (:code:`logger`).
"""
import logging


logger = logging.getLogger('PyFrost')
_handler = logging.StreamHandler()
_formatter = logging.Formatter('[ %(asctime)s ][ %(levelname)s ][ %(name)s ] %(message)s')

_handler.setFormatter(_formatter)
_handler.setLevel(logging.INFO)

logger.addHandler(_handler)
logger.setLevel(logging.INFO)
