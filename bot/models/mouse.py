from enum import IntEnum, auto

from pynput.mouse import Button as PynputButton
from pynput.mouse import Controller as _PynputMouseController

from bot.models.base_model import BotBaseModel, Command, MouseExecutor

_default_mouse_executor: MouseExecutor = _PynputMouseController()


class Button(IntEnum):
    left = auto()
    right = auto()


class MouseClick(BotBaseModel, Command):
    kind: Button
    pos: tuple[int, int]

    def __repr__(self) -> str:
        return f"{self.kind.name.capitalize()} Click: {self.pos}"

    def execute(self, executor: MouseExecutor | None = None):
        mouse = executor or _default_mouse_executor
        mouse.click(getattr(PynputButton, self.kind.name))
