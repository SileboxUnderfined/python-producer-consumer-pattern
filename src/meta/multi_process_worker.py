from logging import Logger
from multiprocessing.connection import Connection
from multiprocessing import Event, Queue
from abc import ABC
from .logger_setup import logger_setup


@logger_setup
class MultiProcessWorker(ABC):
    def __init__(self, conn: Connection, env: dict[str, str], stop_flag: Event, queue: Queue):
        self._connection: Connection = conn # Required for message exchange
        self._env: dict[str, str] = env # environment variables
        self._stop_flag: Event = stop_flag # flag for stopping the application

        self._logger: Logger | None = None