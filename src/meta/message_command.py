from dataclasses import dataclass
from json import loads, dumps

@dataclass
class MessageCommand:
    command: str
    arguments: list[str]

    @staticmethod
    def from_json(data: str):
        data: dict = loads(data)

        return MessageCommand(
            data["command"],
            data["arguments"],
        )

    def to_json(self) -> str:
        data = {"command":self.command,"arguments":self.arguments,}

        return dumps(data)