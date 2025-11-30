from dataclasses import dataclass


@dataclass
class ServerAddress:
    host: str
    port: int
