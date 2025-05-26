from multiprocessing import Queue
from logging.handlers import QueueHandler
import logging

def logger_setup(cls):
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        assert 'queue' in kwargs
        original_init(self, *args, **kwargs)
        queue: Queue = kwargs['queue']

        if self._env['DEBUG'] == '1':
            logger_level = logging.DEBUG
        else:
            logger_level = logging.INFO

        self._logger = logging.getLogger()
        self._logger.setLevel(logger_level)
        self._logger.addHandler(QueueHandler(queue))

    cls.__init__ = new_init
    return cls