from logging import basicConfig, INFO, ERROR
from logging.handlers import TimedRotatingFileHandler
from json import dumps


class StructuredMessage(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return (dumps(self.kwargs))


m = StructuredMessage


# create handler
handler = TimedRotatingFileHandler(
    filename='log/log', when='d', interval=3, backupCount=3, encoding='utf-8', delay=False)

basicConfig(level=INFO, format='{"log_time": "%(asctime)s", "log_lvl": "%(levelname)s", "log_message": %(message)s}',
            datefmt='%d %b %Y %H:%M:%S', handlers=[handler])
