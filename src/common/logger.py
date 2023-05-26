import logging
import sys
import time

COLORS = {
    "DEFAULT": "\033[37m",
    "INFO": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "ENDC": "\033[0m",
}


class LogFormatter(logging.Formatter):
    """Formatter class used for displaying various messages while running the app"""

    def __init__(self, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        t = time.localtime()
        color = COLORS.get(record.levelname, COLORS["DEFAULT"])
        message = logging.Formatter.format(self, record)
        return (
            color
            + "[{}] {}".format(time.strftime("%m/%d/%Y, %H:%M:%S", t), message)
            + COLORS["ENDC"]
        )


logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(LogFormatter())
logger.addHandler(handler)
