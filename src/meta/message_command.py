from dataclasses import dataclass
from json import loads, dumps

@dataclass
class MessageCommand:
    """
    Dataclass that represents Message
    :var command: represents command
    :var arguments: represents arguments for command
    """

    command: str
    arguments: list[str]

    @staticmethod
    def from_json(data: str):
        """
        Deserializes json string to ``MessageCommand`` object
        :param data: data that needs to be deserialized
        :return: ``MessageCommand`` object
        """
        data: dict = loads(data)

        return MessageCommand(
            data["command"],
            data["arguments"],
        )

    def to_json(self) -> str:
        """
        Serializes ``MessageCommand`` object into json string
        :return: ``str``
        """
        data = {"command":self.command,"arguments":self.arguments,}

        return dumps(data)