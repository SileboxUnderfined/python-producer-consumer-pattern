from meta import MessageWorker, MessageCommand, MultiProcessWorker
import time, datetime

class Worker(MultiProcessWorker, MessageWorker):
    def __init__(self, **kwargs):
        MultiProcessWorker.__init__(self, **kwargs)

    def receive_message(self):
        try:
            if not self._connection.poll(timeout=0.1): return

            message: str = self._connection.recv()
            self._logger.info(f"Received message: {message}")
            cmd: MessageCommand = MessageCommand.from_json(message)

            if cmd.command == "hello_request":
                time.sleep(3) # emulating payload
                self.send_message(MessageCommand("hello_response",[f"hi_from_worker! {datetime.datetime.now().time()}"]))
        except KeyboardInterrupt: return

    def send_message(self, message: MessageCommand):
        message: str = message.to_json()

        self._connection.send(message)

        self._logger.info(f"Sent message {message}")

    def mainloop(self):
        while not self._stop_flag.is_set():
            self.receive_message()

        self._logger.info("Worker process successfully stopped!")