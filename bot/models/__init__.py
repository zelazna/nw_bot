from abc import ABC
from dataclasses import dataclass
from typing import Optional

from bot.models.keys_model import KeysModel


@dataclass(frozen=True)
class BaseKey(ABC):
    key: str
    scan_code: int


@dataclass(frozen=True)
class ModifierKey(BaseKey): ...


@dataclass(frozen=True)
class Keystroke(BaseKey):
    modifier: Optional[ModifierKey] = None

    def __repr__(self) -> str:
        if self.modifier:
            return f"{self.modifier.key}+{self.key}"
        return self.key


@dataclass
class Params:
    limit: int
    keys: list[Keystroke]
    win_num: int
    interval: str

    @property
    def interval_range(self) -> list[int]:
        if "-" in self.interval:
            min, max = self.interval.split("-")
            interval_range = list(range(int(min), int(max)))
        else:
            interval_range = [int(self.interval)]
        return interval_range


__all__ = ["KeysModel", "Params", "ModifierKey", "Keystroke"]
