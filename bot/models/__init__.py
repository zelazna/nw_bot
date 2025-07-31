from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pynput.keyboard import KeyCode
from pynput.mouse import Button

from bot.models.commands import CommandsModel


if TYPE_CHECKING:
    from pynput.keyboard import Controller as KeyBoardController
    from pynput.mouse import Controller as MouseController


class BaseCommand(ABC):
    @abstractmethod
    def execute(self): ...


@dataclass
class BaseKey:
    key: str
    vk: int

    @property
    def key_code(self) -> KeyCode:
        return KeyCode.from_vk(self.vk)


class ModifierKey(BaseKey): ...


@dataclass
class Keystroke(BaseKey, BaseCommand):
    controller: "KeyBoardController"
    modifier: ModifierKey | None = None

    def __repr__(self) -> str:
        try:
            key_repr = self.key.split("_")[1]
        except IndexError:
            key_repr = self.key
        if self.modifier:
            return f"{self.modifier.key.capitalize()}+{key_repr}"
        return key_repr.capitalize()

    def execute(self):
        if self.modifier:
            self.controller.press(self.modifier.key_code)
        try:
            self.controller.tap(self.key_code)
        finally:
            if self.modifier:
                self.controller.release(self.modifier.key_code)


@dataclass
class MouseClick(BaseCommand):
    kind: Button
    pos: tuple[int, int]
    controller: "MouseController"

    def __repr__(self) -> str:
        return f"{self.kind.name.capitalize()} Click: {self.pos}"

    def execute(self):
        self.controller.click(self.kind)


@dataclass
class Params:
    limit: float | int
    commands: list[BaseCommand]
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


__all__ = [
    "CommandsModel",
    "Params",
    "ModifierKey",
    "Keystroke",
    "MouseClick",
    "BaseCommand",
]
