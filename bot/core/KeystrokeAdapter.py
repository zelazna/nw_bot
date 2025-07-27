from typing import cast

from pynput.keyboard import Key
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from bot.models import Keystroke, ModifierKey

ALT_VK = cast(int, Key.alt.value.vk)
TAB_VK = cast(int, Key.tab.value.vk)
CTRL_VK = cast(int, Key.ctrl.value.vk)
SHIFT_VK = cast(int, Key.shift.value.vk)
DEL_VK = cast(int, Key.delete.value.vk)


directionalMapping = {
    Key.up.value.vk: Key.up,
    Key.down.value.vk: Key.down,
    Key.left.value.vk: Key.left,
    Key.right.value.vk: Key.right,
}

ALT_TAB = Keystroke(key="Tab", modifier=ModifierKey(key="Alt", vk=ALT_VK), vk=TAB_VK)


def match(event: QKeyEvent) -> Keystroke | None:
    modifier = event.modifiers()
    vk = event.nativeVirtualKey()
    override = None

    if vk in (CTRL_VK, ALT_VK, DEL_VK):
        # Ignore CTRL and ALT keys as they are modifiers
        return None

    if vk in directionalMapping:
        override = directionalMapping[vk]

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
    return Keystroke(key=key.name, vk=vk, modifier=mod, override=override)
