
from pynput.keyboard import Controller as KeyBoardController
from pynput.keyboard import Key
from pynput.mouse import Controller as MouseController
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from bot.core.constants import ALT_VK, CTRL_VK, DEL_VK, SHIFT_VK
from bot.models import Keystroke, ModifierKey

directionalMapping = {k.value.vk: k for k in (Key.up, Key.down, Key.left, Key.right)}
mouse = MouseController()
keyboard = KeyBoardController()


def match(event: QKeyEvent) -> Keystroke | None:
    modifier = event.modifiers()
    vk = event.nativeVirtualKey()

    if vk in (CTRL_VK, ALT_VK, DEL_VK):
        # Ignore CTRL and ALT keys as they are modifiers
        return None

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
    return Keystroke(key.name, vk, mod)
