from typing import cast

from pynput.keyboard import Key
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from bot.models import Keystroke, ModifierKey
from bot.utils import logger

ALT_VK = cast(int, Key.alt.value.vk)
TAB_VK = cast(int, Key.tab.value.vk)
CTRL_VK = cast(int, Key.ctrl.value.vk)
SHIFT_VK = cast(int, Key.shift.value.vk)
DEL_VK = cast(int, Key.delete.value.vk)
ALT_TAB = Keystroke(key="Tab", modifier=ModifierKey("Alt", ALT_VK), vk=TAB_VK)


def match(event: QKeyEvent) -> Keystroke | None:
    modifier = event.modifiers()
    vk = event.nativeVirtualKey()
    if vk in (CTRL_VK, ALT_VK, DEL_VK):
        # Ignore CTRL and ALT keys as they are modifiers
        return None

    try:
        key = Qt.Key(event.key())
        logger.debug(
            f"Matching key event: {event}, key: {key}, vk: {vk}, modifier: {modifier}"
        )
        mod = None
        if modifier is not Qt.KeyboardModifier.NoModifier:
            match modifier:
                case Qt.KeyboardModifier.ControlModifier:
                    mod = ModifierKey("Ctrl", CTRL_VK)
                case Qt.KeyboardModifier.AltModifier:
                    mod = ModifierKey("Alt", ALT_VK)
                case Qt.KeyboardModifier.ShiftModifier:
                    mod = ModifierKey("Shift", SHIFT_VK)
                case _:
                    pass
        return Keystroke(key.name, vk, mod)
    except ValueError:
        logger.error(f"Invalid key event: {event}")
    except Exception as e:
        logger.error(f"Error matching key event: {e}")
