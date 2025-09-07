from pydantic import ConfigDict, Field

from bot.models import DirectionalKeystroke, Keystroke, MouseClick
from bot.models.base_model import BotBaseModel


class Params(BotBaseModel):
    model_config = ConfigDict(frozen=True)
    commands: tuple[Keystroke | DirectionalKeystroke | MouseClick, ...] = Field(
        default_factory=tuple
    )
    winNum: int = 1
    limit: int = 5
    interval: str = "1"

    @property
    def interval_range(self) -> list[int]:
        if "-" in self.interval:
            min, max = self.interval.split("-")
            interval_range = list(range(int(min), int(max) + 1))
        else:
            interval_range = [int(self.interval)]
        return interval_range

    def __repr__(self) -> str:
        cmds = [f"{cmd!r}\n" for cmd in self.commands]

        return f"""winNum {self.winNum}
limit {self.limit}
interval {self.interval}

{"".join(cmds)}
"""
