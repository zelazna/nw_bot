from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, cast

from pynput.keyboard import Key, KeyCode
from PySide6.QtCore import QElapsedTimer, Qt
from PySide6.QtGui import QKeyEvent

from bot.core.constants import ALT_VK, CTRL_VK, DEL_VK, SHIFT_VK
from bot.models import (
    CommandListModel,
    DirectionalKeystroke,
    Keystroke,
    ModifierKey,
    Timer,
)
from bot.utils.logger import logger

PynputEvent = Key | KeyCode | None


@dataclass
class BaseKeyStrokeAdapter(ABC):
    model: CommandListModel
    directionalMapping = {
        k.value.vk: k for k in (Key.up, Key.down, Key.left, Key.right)
    }

    @abstractmethod
    def on_key_press(self, event: Any): ...

    @abstractmethod
    def on_key_release(self, event: Any): ...


class QtKeystrokeAdapter(BaseKeyStrokeAdapter):
    upper_keys = ("&", "é", '"', "'", "(", "-", "è", "_", "ç", "à", ")", "=")

    def on_key_press(self, event: Any): ...
    def on_key_release(self, event: QKeyEvent):
        modifier = event.modifiers()
        vk: int = event.nativeVirtualKey()

        if vk in (CTRL_VK, ALT_VK, DEL_VK):
            # Ignore CTRL and ALT keys as they are modifiers
            return None

        if vk in self.directionalMapping:
            keystroke = DirectionalKeystroke(key=self.directionalMapping[vk].name)
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

        if event.text() in self.upper_keys:
            keystroke = Keystroke(key=event.text())
        else:
            keystroke = Keystroke(key=key.name, vk=vk, modifier=mod)
        self.model.commands.append(keystroke)
        self.model.layoutChanged.emit()


class PynputKeystrokeAdapter(BaseKeyStrokeAdapter):
    timer = QElapsedTimer()
    modifier: PynputEvent = None
    current_key: PynputEvent = None
    modifiers = (
        Key.shift,
        Key.alt,
        Key.alt_l,
        Key.ctrl,
        Key.ctrl_l,
        Key.cmd,
    )

    def on_key_press(self, event: PynputEvent):
        if not event or event == self.current_key:
            return

        self.current_key = event
        self.timer.start()

        if event in self.modifiers:
            logger.debug(f"got modifier key: {event!r} storing it for know")
            self.modifier = event
            return

    def on_key_release(self, event: PynputEvent):
        if event in self.modifiers:
            self.modifier = None
            return

        try:
            timer = Timer(milliseconds=self.timer.elapsed())
            if not self.modifier:
                logger.debug(f"Get single key: {event!r}")
                if isinstance(event, Key):
                    if event.value.vk in self.directionalMapping:
                        self.model.commands.append(
                            DirectionalKeystroke(key=event.name, hold=timer)
                        )
                    elif event.value.vk:
                        self.model.commands.append(
                            Keystroke(key=event.name, vk=event.value.vk, hold=timer)
                        )
                elif isinstance(event, KeyCode):
                    self.model.commands.append(
                        Keystroke(key=cast(str, event.char), vk=event.vk, hold=timer)
                    )
            else:
                logger.debug(
                    f"Modifier detected along key mod: {self.modifier!r}, key: {event!r}"
                )
                modifier = ModifierKey(
                    key=self.modifier.name,  # type: ignore
                    vk=self.modifier.value.vk,  # type: ignore
                )

                if self.modifier in (Key.ctrl, Key.ctrl_l):
                    key = self._decode_ctrl_char(event.char)  # type: ignore
                else:
                    key = event.value.char if isinstance(event, Key) else event.char  # type: ignore

                self.model.commands.append(
                    Keystroke(key=key, vk=event.vk, modifier=modifier, hold=timer)  # type: ignore
                )
            self.current_key = None
            self.model.layoutChanged.emit()

        except AttributeError:
            logger.error(f"Unhandled key: {event!r}", exc_info=True)

    def _decode_ctrl_char(self, char: str) -> str:
        val = ord(char)
        if 1 <= val <= 26:
            return chr(val + 64)  # Ex: \x01 => Ctrl + A
        return char
