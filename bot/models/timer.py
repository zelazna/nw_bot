import time
from dataclasses import dataclass

from bot.models.base_command import BaseCommand
from bot.utils import format_time


@dataclass
class Timer(BaseCommand):
    milliseconds: int = 200

    def __repr__(self) -> str:
        return format_time(self.milliseconds)[3:]

    @property
    def seconds(self) -> float:
        return self.milliseconds / 1000

    def execute(self):
        time.sleep(self.seconds)
