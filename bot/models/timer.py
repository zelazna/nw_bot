import random
import time
from typing import ClassVar, final, override

from bot.models.base_model import BotBaseModel, Command


@final
class SleepCommand(BotBaseModel, Command):
    milliseconds: int = 200

    @override
    def __repr__(self) -> str:
        return str(self.milliseconds)

    @property
    def seconds(self) -> float:
        return self.milliseconds / 1000

    @override
    def execute(self) -> None:
        time.sleep(self.seconds)


@final
class SleepRandomCommand(BotBaseModel, Command):
    is_reportable: ClassVar[bool] = False
    interval_range: list[int]

    @override
    def execute(self) -> None:
        time.sleep(random.choice(self.interval_range))
