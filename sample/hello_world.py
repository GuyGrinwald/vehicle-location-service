import os
import logging
import logging.config

logging.config.fileConfig('logging.conf')

logger = logging.getLogger(__name__)

print("Hello, World!")
logger.info("Hello, World!")