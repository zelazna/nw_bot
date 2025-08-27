from dataclasses import dataclass
from enum import IntEnum, auto
from typing import ClassVar

from pynput.mouse import Button as PynoutButton
from pynput.mouse import Controller


class Button(IntEnum):
    left = auto()
    right = auto()


@dataclass(frozen=True)
class MouseClick:
    kind: Button
    pos: tuple[int, int]
    controller: ClassVar[Controller] = Controller()

    def __repr__(self) -> str:
        return f"{self.kind.name.capitalize()} Click: {self.pos}"

    def execute(self):
        button = getattr(PynoutButton, self.kind.name)
        self.controller.press(button)
        self.controller.release(button)
