from enum import IntEnum, auto
from typing import final, override

from pynput.mouse import Button as PynputButton
from pynput.mouse import Controller as _PynputMouseController

from bot.models.base_model import BotBaseModel, Command, MouseExecutor

_default_mouse_executor: MouseExecutor = _PynputMouseController()  # pyright: ignore[reportAssignmentType]


class Button(IntEnum):
    left = auto()
    right = auto()


@final
class MouseClick(BotBaseModel, Command):
    kind: Button
    pos: tuple[int, int]

    @override
    def __repr__(self) -> str:
        return f"{self.kind.name.capitalize()} Click: {self.pos}"

    @override
    def execute(self, executor: MouseExecutor | None = None) -> None:  # type: ignore[override]
        mouse = executor or _default_mouse_executor
        mouse.click(getattr(PynputButton, self.kind.name))  # pyright: ignore[reportAny]
