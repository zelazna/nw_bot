from dataclasses import dataclass, field

from bot.models.base_command import BaseCommand


@dataclass
class Params:
    commands: list[BaseCommand] = field(default_factory=list)
    winNum: int = 1
    limit: float | int = 5
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
