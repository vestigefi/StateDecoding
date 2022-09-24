import logging
import sys
import time


class LogFormatter(logging.Formatter):
    """Formatter class used for displaying various messages while running the app"""

    def __init__(self, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        t = time.localtime()
        message = logging.Formatter.format(self, record)
        return "[{}] {}:{}".format(
            time.strftime("%m/%d/%Y, %H:%M:%S", t), record.levelname, message
        )


logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(LogFormatter())
logger.addHandler(handler)
