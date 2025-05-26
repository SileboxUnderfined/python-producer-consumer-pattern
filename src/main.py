from multiprocessing import Process, Pipe, Event, Queue
from waitress import serve as waitress_serve
from logging import Logger, StreamHandler, Formatter
from logging.handlers import QueueListener
from os import environ
from server import Server
from worker import Worker
import logging, signal

def start_worker(**kwargs):
    """
    Function to start Worker process
    :param kwargs: params for Worker class
    :return: None
    """

    w = Worker(**kwargs)
    w.mainloop()

def start_server(**kwargs):
    """
    Function to start Server process. if environment variable ``DEBUG`` is ``1``, then it starts
    flask werkzeug server, else - waitress production WSGI server.
    :param kwargs: params for Server class
    :return: None
    """

    s = Server(**kwargs)

    if kwargs['env']['DEBUG'] == '1':
        s.run(host="127.0.0.1",port=8000)
    else:
        waitress_serve(s,host=kwargs['env']['WAITRESS_HOST'],port=kwargs['env']['WAITRESS_PORT'])

def setup_env(keys: list[str]) -> dict[str, str]:
    """
    Function that brings ``keys`` and ``values`` from ``os.environ``
    and returns dictionary with these values.
    :param keys: keys that need to be brought from ``os.environ``
    :return: Dictionary with keys and values from ``os.environ``
    """

    result = {}
    for key in keys:
        if key in environ: result[key] = environ[key]

    return result

def check_env():
    assert 'DEBUG' in environ
    assert 'WAITRESS_HOST' in environ
    assert 'WAITRESS_PORT' in environ

def grateful_exit(signum, frame):
    """
    Function that gratefully stops processes using ``Event`` mechanism of ``multiprocessing``
    :param signum:
    :param frame:
    :return: None
    """

    logger.info("Stopping processes...")
    stop_flag.set()


if __name__ == "__main__":
    check_env() # check env

    # logging setup
    logging_level = logging.DEBUG if environ['DEBUG'] == '1' else logging.INFO

    logger: Logger = logging.getLogger()
    logger.setLevel(logging_level)
    formatter: Formatter = logging.Formatter('[%(asctime)s] [%(levelname)s/%(processName)s] [%(module)s.%(funcName)s] %(message)s')
    console_handler: StreamHandler = StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    log_queue: Queue = Queue()
    queue_listener: QueueListener = QueueListener(log_queue, console_handler)
    queue_listener.start()

    # env setup
    server_env = setup_env(['DEBUG','WAITRESS_HOST','WAITRESS_PORT'])
    worker_env = setup_env(['DEBUG'])

    # processes setup
    worker_conn, server_conn = Pipe()
    stop_flag: Event = Event()
    worker_process = Process(target=start_worker,kwargs={'conn': worker_conn, 'env': worker_env, 'stop_flag': stop_flag, 'queue': log_queue},name="Worker")
    server_process = Process(target=start_server,kwargs={'conn': server_conn, 'env': server_env, 'stop_flag': stop_flag, 'queue': log_queue},name="Server")

    signal.signal(signal.SIGINT, grateful_exit)
    signal.signal(signal.SIGTERM, grateful_exit)

    # processes start
    worker_process.start()
    server_process.start()

    worker_process.join()
    server_process.join()