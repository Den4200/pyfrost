import logging


logger = logging.getLogger('PyFrost')
handler = logging.StreamHandler()
formatter = logging.Formatter('[ %(asctime)s ][ %(levelname)s ][ %(name)s ] %(message)s')

handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger.addHandler(handler)
logger.setLevel(logging.INFO)
