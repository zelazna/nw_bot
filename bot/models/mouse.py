from enum import IntEnum, auto
from typing import ClassVar

from pynput.mouse import Button as PynoutButton
from pynput.mouse import Controller

from bot.models.base_model import BotBaseModel


class Button(IntEnum):
    left = auto()
    right = auto()


class MouseClick(BotBaseModel):
    kind: Button
    pos: tuple[int, int]
    controller: ClassVar[Controller] = Controller()

    def __repr__(self) -> str:
        return f"{self.kind.name.capitalize()} Click: {self.pos}"

    def execute(self):
        self.controller.click(getattr(PynoutButton, self.kind.name))
