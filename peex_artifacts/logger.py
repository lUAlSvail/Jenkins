import logging, logging.config
# set up logging
logging.config.fileConfig("logging.ini")
logger = logging.getLogger('sLogger')
# log something
logger.debug('debug')
logger.info('info')
logger.warning('warning')
logger.error('error')
logger.critical('criticals')