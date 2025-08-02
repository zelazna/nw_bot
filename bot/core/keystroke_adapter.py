from abc import ABC, abstractmethod
from typing import Any

from pynput.keyboard import Controller as KeyBoardController
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Controller as MouseController
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from bot.core.constants import ALT_VK, CTRL_VK, DEL_VK, SHIFT_VK
from bot.core.worker import WorkerSignals
from bot.models import (
    CommandsModel,
    DirectionalKeystroke,
    Keystroke,
    ModifierKey,
    dataclass,
)
from bot.utils.logger import logger

directionalMapping = {k.value.vk: k for k in (Key.up, Key.down, Key.left, Key.right)}
mouse = MouseController()
keyboard = KeyBoardController()
MODIFIERS = [
    Key.shift,
    Key.alt,
    Key.alt_l,
    Key.ctrl,
    Key.ctrl_l,
    Key.cmd,
]


@dataclass
class KeyStrokeAdapter(ABC):
    model: CommandsModel

    @abstractmethod
    def on_key_press(self, event: Any): ...

    @abstractmethod
    def on_key_release(self, event: Any): ...


@dataclass
class QTKeystrokeAdapter(KeyStrokeAdapter):
    def on_key_press(self, event: Any): ...
    def on_key_release(self, event: QKeyEvent):
        modifier = event.modifiers()
        vk: int = event.nativeVirtualKey()

        if vk in (CTRL_VK, ALT_VK, DEL_VK):
            # Ignore CTRL and ALT keys as they are modifiers
            return None

        if vk in directionalMapping:
            keystroke = DirectionalKeystroke(directionalMapping[vk].name)
            self.model.commands.append(keystroke)
            self.model.layoutChanged.emit()
            return

        key = Qt.Key(event.key())

        mod = None
        if modifier is not Qt.KeyboardModifier.NoModifier:
            match modifier:
                case Qt.KeyboardModifier.ControlModifier:
                    mod = ModifierKey(key="Ctrl", vk=CTRL_VK)
                case Qt.KeyboardModifier.AltModifier:
                    mod = ModifierKey(key="Alt", vk=ALT_VK)
                case Qt.KeyboardModifier.ShiftModifier:
                    mod = ModifierKey(key="Shift", vk=SHIFT_VK)
                case _:
                    pass
        keystroke = Keystroke(key=key.name, vk=vk, modifier=mod)
        self.model.commands.append(keystroke)
        self.model.layoutChanged.emit()


@dataclass
class PynputKeystrokeAdapter(KeyStrokeAdapter):
    modifier: Key | None = None
    signals = WorkerSignals()

    def on_key_press(self, event: Key | KeyCode | None):
        if not event:
            return

        if event in MODIFIERS:
            logger.debug(f"got modifier key: {event!r} ignoring it for know")
            self.modifier = event
            return

        try:
            if not self.modifier:
                logger.debug(f"Get single key: {event!r}")

                if isinstance(event, Key) and event.value.vk in directionalMapping:
                    self.model.commands.append(DirectionalKeystroke(event.name))
                elif isinstance(event, KeyCode):
                    self.model.commands.append(Keystroke(event.char, event.vk))
            else:
                logger.debug(
                    f"Modifier detected along key mod: {self.modifier!r}, key: {event!r}"
                )
                modifier = ModifierKey(
                    key=self.modifier.name, vk=self.modifier.value.vk
                )

                if self.modifier in (Key.ctrl, Key.ctrl_l):
                    key = self._decode_ctrl_char(event.char)
                else:
                    key = event.value.char if isinstance(event, Key) else event.char

                self.model.commands.append(Keystroke(key, event.vk, modifier))
            self.model.layoutChanged.emit()

        except AttributeError:
            logger.error(f"Unhandled key: {event!r}", exc_info=True)

    def on_key_release(self, event: Key | KeyCode | None):
        if event in MODIFIERS:
            self.modifier = None

    def _decode_ctrl_char(self, char: str) -> str:
        val = ord(char)
        if 1 <= val <= 26:
            return chr(val + 64)  # Ex: \x01 => Ctrl + A
        return char
