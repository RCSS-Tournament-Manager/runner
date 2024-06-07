import colorlog
import logging
import asyncio


DEBUG_ENV = False
getLogger = colorlog.getLogger
DEBUG = colorlog.DEBUG
INFO = colorlog.INFO
WARNING = colorlog.WARNING
ERROR = colorlog.ERROR
CRITICAL = colorlog.CRITICAL

colorlog.basicConfig(
    format='%(log_color)s%(asctime)s:%(levelname)s:%(name)s - %(message)s',
    datefmt='%Y-%m-%d-%H:%M:%S',
    level=colorlog.DEBUG if DEBUG_ENV else colorlog.INFO
)


def init_logger(name='root'):
    logger = logging.getLogger(name)
    
    _muted = colorlog.INFO if DEBUG_ENV else colorlog.WARNING
    _shut_upped = colorlog.ERROR if DEBUG_ENV else colorlog.CRITICAL
    # getLogger('urllib3.connectionpool').setLevel(_muted)
    _logger = getLogger('watchdog')
    # getLogger('apscheduler').setLevel(colorlog.WARNING)
    
    return logger


def get_logger(name):
    return init_logger(name)
