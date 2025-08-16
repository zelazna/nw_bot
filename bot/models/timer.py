import time
from dataclasses import dataclass


@dataclass
class Timer:
    milliseconds: int = 200

    def __repr__(self) -> str:
        return str(self.milliseconds)

    @property
    def seconds(self) -> float:
        return self.milliseconds / 1000

    def execute(self):
        time.sleep(self.seconds)
