from typing import Optional

from pydantic import BaseModel
from pynput.keyboard import KeyCode, Key
from pynput.mouse import Button

from bot.models.CommandsModel import CommandsModel


class BaseKey(BaseModel):
    key: str
    vk: int

    @property
    def key_code(self) -> KeyCode:
        return KeyCode.from_vk(self.vk)


class ModifierKey(BaseKey): ...


class Keystroke(BaseKey):
    modifier: Optional[ModifierKey] = None
    override: Optional[Key] = None

    def __repr__(self) -> str:
        try:
            key_repr = self.key.split("_")[1]
        except IndexError:
            key_repr = self.key
        if self.modifier:
            return f"{self.modifier.key}+{key_repr}"
        return key_repr


class Params(BaseModel):
    limit: float | int
    commands: list["Keystroke | MouseClick"]
    winNum: int
    interval: str

    @property
    def interval_range(self) -> list[int]:
        if "-" in self.interval:
            min, max = self.interval.split("-")
            interval_range = list(range(int(min), int(max) + 1))
        else:
            interval_range = [int(self.interval)]
        return interval_range


class MouseClick(BaseModel):
    kind: Button
    pos: tuple[int, int]

    def __repr__(self) -> str:
        return f"{self.kind.name.capitalize()} Click: {self.pos}"


__all__ = ["CommandsModel", "Params", "ModifierKey", "Keystroke", "MouseClick"]
