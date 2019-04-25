import logging
import sys


logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)


class Task(object):
    def __init__(self, flowline, verbose=False):
        self.name = self.__class__.__name__
        self.flowline = flowline
        self.verbose = verbose

    def run(self, context):
        return context

    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        if self.verbose:
            logger.setLevel(logging.DEBUG)
        return logger
