import logging


logger = logging.getLogger('PyFrost')
logger.basicConfig(
    format='[ %(asctime)s ][ %(levelname)s ][ %(name)s ] %(message)s',
    level=logging.INFO
)
