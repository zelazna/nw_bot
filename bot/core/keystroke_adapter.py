from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from bot.core.constants import ALT_VK, CTRL_VK, TAB_VK, DEL_VK
from bot.models import Keystroke, ModifierKey
from bot.utils import logger

ALT_TAB = Keystroke(key="TAB", modifier=ModifierKey("ALT", ALT_VK), vk=TAB_VK)


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
        if modifier is not Qt.KeyboardModifier.NoModifier:
            match modifier:
                case Qt.KeyboardModifier.ControlModifier:
                    return Keystroke(
                        key=key.name,
                        vk=vk,
                        modifier=ModifierKey("CTRL", CTRL_VK),
                    )

                case Qt.KeyboardModifier.AltModifier:
                    return Keystroke(
                        key=key.name,
                        vk=vk,
                        modifier=ModifierKey("ALT", ALT_VK),
                    )
                case _:
                    pass
        return Keystroke(key.name, vk)
    except ValueError:
        logger.error(f"Invalid key event: {event}")
    except Exception as e:
        logger.error(f"Error matching key event: {e}")
