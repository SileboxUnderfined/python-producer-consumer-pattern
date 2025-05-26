from flask import Flask
from meta import MessageWorker, MessageCommand, MultiProcessWorker
import logging


class Server(Flask, MultiProcessWorker, MessageWorker):
    """
    Server's class. All interaction with user must be described here.
    """

    def __init__(self, **kwargs):
        """
        Constructor of Server's class. It calls constructors of super classes, then setups logging
        and after that setups url rules.
        :param kwargs: arguments for ``MultiProcessWorker`` constructor
        """
        
        Flask.__init__(self, __name__)
        MultiProcessWorker.__init__(self, **kwargs)

        if self._env['DEBUG'] == '1':
            logging.getLogger('werkzeug').handlers.clear()
            logging.getLogger('werkzeug').addHandler(self._logger.handlers[0])
        else:
            logging.getLogger('waitress').handlers.clear()
            logging.getLogger('waitress').addHandler(self._logger.handlers[0])


        # use self.add_url_rule to add url rules...

        self.add_url_rule("/hello_world",view_func=Server.hello_world) # You can write static...
        self.add_url_rule("/hello_from_worker",view_func=self.get_hello_from_worker) # Or non-static methods...

    def receive_message(self) -> str:
        message: str = self._connection.recv()
        self._logger.info(f"Received message: {message}")
        cmd: MessageCommand = MessageCommand.from_json(message)

        if cmd.command == "hello_response":
            return cmd.arguments[0]

    def send_message(self, message: MessageCommand):
        message: str = message.to_json()

        self._connection.send(message)

        self._logger.info(f"Sent message: {message}")

    @staticmethod
    def hello_world():
        return "<h1>Hello, World!</h1>"

    def get_hello_from_worker(self):
        self.send_message(MessageCommand("hello_request",[]))
        data: str = self.receive_message()

        return data