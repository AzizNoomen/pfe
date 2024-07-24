import sys
from loguru import logger

# Configure the logger to output to console only
logger.remove()  # Remove the default configuration

logger.add(sink=sys.stdout, level="DEBUG", backtrace=True, diagnose=True, catch=True)
