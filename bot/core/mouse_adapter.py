from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import Qt
from pynput.mouse import Button as PynputButton
from bot.models import Button, CommandListModel, MouseClick
from bot.utils.logger import logger


@dataclass
class BaseMouseAdapter(ABC):
    model: CommandListModel

    @abstractmethod
    def on_click(self, x: int, y: int, button: Any, pressed: bool): ...


class QtMouseAdapter(BaseMouseAdapter):
    def on_click(self, x: int, y: int, button: Qt.MouseButton, pressed: bool):
        kind = Button.right if button is Qt.MouseButton.RightButton else Button.left
        self.model.commands.append(MouseClick(kind, (x, y)))
        self.model.layoutChanged.emit()


class PynputMouseAdapter(BaseMouseAdapter):
    def on_click(self, x: int, y: int, button: PynputButton, pressed: bool):
        if pressed:
            try:
                self.model.commands.append(
                    MouseClick(kind=Button[button.name], pos=(x, y))
                )
                self.model.layoutChanged.emit()
            except KeyError:
                logger.error(f"Unknow button {button}")
