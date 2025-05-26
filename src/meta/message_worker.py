from abc import ABC, abstractmethod
from .message_command import MessageCommand

class MessageWorker(ABC):
    """
    Interface to implement messaging between processes
    """

    @abstractmethod
    def receive_message(self):
        """
        Method to receive message
        :return: None or ``str``
        """

        pass

    @abstractmethod
    def send_message(self, message: MessageCommand):
        """
        Method to send message
        :param message: ``MessageCommand`` object which represents message to send
        :return: None
        """

        pass