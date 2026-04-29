import random
import time
from typing import ClassVar

from bot.models.base_model import BotBaseModel, Command


class SleepCommand(BotBaseModel, Command):
    milliseconds: int = 200

    def __repr__(self) -> str:
        return str(self.milliseconds)

    @property
    def seconds(self) -> float:
        return self.milliseconds / 1000

    def execute(self):
        time.sleep(self.seconds)


class SleepRandomCommand(BotBaseModel, Command):
    is_reportable: ClassVar[bool] = False
    interval_range: list[int]

    def execute(self) -> None:
        time.sleep(random.choice(self.interval_range))
