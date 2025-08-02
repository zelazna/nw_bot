from abc import ABC, abstractmethod
from typing import Any

from pynput.keyboard import Controller as KeyBoardController
from pynput.keyboard import Key
from pynput.mouse import Controller as MouseController
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from bot.core.constants import ALT_VK, CTRL_VK, DEL_VK, SHIFT_VK
from bot.models import (
    BaseKey,
    CommandsModel,
    DirectionalKeystroke,
    Keystroke,
    ModifierKey,
)

directionalMapping = {k.value.vk: k for k in (Key.up, Key.down, Key.left, Key.right)}
mouse = MouseController()
keyboard = KeyBoardController()


class KeyStrokeAdapter(ABC):
    def __init__(self, model: CommandsModel) -> None:
        self.model = model

    @abstractmethod
    def on_key_press(self, event: Any): ...

    @abstractmethod
    def on_key_release(self, event: Any): ...


class QTKeystrokeAdapter(KeyStrokeAdapter):
    def on_key_press(self, event: Any):
        modifier = event.modifiers()
        vk = event.nativeVirtualKey()

        if vk in (CTRL_VK, ALT_VK, DEL_VK):
            # Ignore CTRL and ALT keys as they are modifiers
            return None

        key = Qt.Key(event.key())

        if vk in directionalMapping:
            keystroke = DirectionalKeystroke(key=directionalMapping[vk].name, vk=vk)

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

    def on_key_release(self, event: Any): ...


def match(event: QKeyEvent) -> BaseKey | None:
    modifier = event.modifiers()
    vk = event.nativeVirtualKey()

    if vk in (CTRL_VK, ALT_VK, DEL_VK):
        # Ignore CTRL and ALT keys as they are modifiers
        return None

    key = Qt.Key(event.key())

    if vk in directionalMapping:
        return DirectionalKeystroke(key=directionalMapping[vk].name, vk=vk)

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
    return Keystroke(key.name, vk, mod)
