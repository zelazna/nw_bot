from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import ClassVar

from pynput.keyboard import KeyCode, Key
from pynput.mouse import Button as PynoutButton
from pynput.keyboard import Controller as KeyBoardController
from pynput.mouse import Controller as MouseController

from bot.models.commands import CommandsModel

directionalMapping = {k.value.vk: k for k in (Key.up, Key.down, Key.left, Key.right)}


class BaseCommand(ABC):
    @abstractmethod
    def execute(self): ...


@dataclass
class BaseKey:
    key: str
    vk: int

    @property
    def key_code(self) -> KeyCode | Key:
        return KeyCode.from_vk(self.vk)


class ModifierKey(BaseKey): ...


@dataclass
class Keystroke(BaseKey, BaseCommand):
    modifier: ModifierKey | None = None
    controller: ClassVar[KeyBoardController] = KeyBoardController()

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


class Button(IntEnum):
    left = auto()
    right = auto()


@dataclass
class MouseClick(BaseCommand):
    kind: Button
    pos: tuple[int, int]
    controller: ClassVar[MouseController] = MouseController()

    def __repr__(self) -> str:
        return f"{self.kind.name.capitalize()} Click: {self.pos}"

    def execute(self):
        self.controller.click(getattr(PynoutButton, self.kind.name))


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


class DirectionalKeystroke(BaseKey):
    @property
    def key_code(self) -> Key:
        return directionalMapping[self.vk]

    def __repr__(self) -> str:
        match self.key:
            case "up":
                return "↑"
            case "down":
                return "↓"
            case "left":
                return "←"
            case "right":
                return "→"
            case _:
                return "Unknow"


__all__ = [
    "CommandsModel",
    "Params",
    "ModifierKey",
    "Keystroke",
    "MouseClick",
    "BaseCommand",
]
