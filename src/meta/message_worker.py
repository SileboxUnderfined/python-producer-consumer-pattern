from abc import ABC, abstractmethod
from .message_command import MessageCommand

class MessageWorker(ABC):
    @abstractmethod
    def receive_message(self): pass

    @abstractmethod
    def send_message(self, message: MessageCommand): pass