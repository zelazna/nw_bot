from dataclasses import dataclass

from pynput.mouse import Button as PynputButton
from PySide6.QtCore import Qt

from bot.models import Button, CommandListModel, MouseClick
from bot.utils.logger import logger


@dataclass
class MouseAdapter:
    model: CommandListModel

    def on_click(
        self, x: int, y: int, button: Qt.MouseButton | PynputButton, pressed: bool
    ):
        match button:
            case Qt.MouseButton.RightButton | PynputButton.right:
                kind = Button.right
            case Qt.MouseButton.LeftButton | PynputButton.left:
                kind = Button.left
            case _:
                logger.error(f"Unknow button {button}")
                return
        self.model.commands.append(MouseClick(kind, (x, y)))
        self.model.layoutChanged.emit()
