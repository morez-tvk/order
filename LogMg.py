import logging

# create logger with 'spam_application'
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('order')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
# fh = logging.FileHandler('controller.log')

# add a rotating handler
fh = RotatingFileHandler('order.log', maxBytes=2000000,
                              backupCount=10)


fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
#ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
#logger.addHandler(ch)

