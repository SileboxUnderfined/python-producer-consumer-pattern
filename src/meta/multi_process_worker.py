from logging import Logger
from multiprocessing.connection import Connection
from multiprocessing import Event, Queue
from abc import ABC
from .logger_setup import logger_setup


@logger_setup
class MultiProcessWorker(ABC):
    """
    ``MultiProcessWorker`` is an abstract class, that handles initializing common
    fields of ``Server`` and ``Worker`` classes.
    :var self._connection: Connection between ``Server`` and ``Worker`` processes
    :var self._env: Environment variables
    :var self._stop_flag: ``multiprocessing.Event`` object to stop process gratefully
    :var self._logger: ``logging.Logger`` object to log messages
    """

    def __init__(self, conn: Connection, env: dict[str, str], stop_flag: Event, queue: Queue):
        """

        :param conn: Connection, which used by processes to exchange messages
        :param env: Environment variables
        :param stop_flag: ``multiprocessing.Event`` to gratefully stop process. Executed from ``MainProcess``
        :param queue: ``multiprocessing.Queue`` for logging by ``multiprocessing.QueueHandler`` and ``multiprocessing.QueueListener``
        """

        self._connection: Connection = conn # Required for message exchange
        self._env: dict[str, str] = env # environment variables
        self._stop_flag: Event = stop_flag # flag for stopping the application

        self._logger: Logger | None = None