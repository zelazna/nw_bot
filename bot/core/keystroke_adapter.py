from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from bot.core.constants import ALT, CTRL, TAB
from bot.models import Keystroke, ModifierKey
from bot.utils import logger


ALT_TAB = Keystroke(key="TAB", scan_code=TAB, modifier=ModifierKey("ALT", ALT))


def match(event: QKeyEvent) -> Keystroke | None:
    modifier = event.modifiers()
    scan_code = event.nativeScanCode()

    if scan_code in (CTRL, ALT):
        # Ignore CTRL and ALT keys as they are modifiers
        return None

    try:
        key = Qt.Key(event.key())
        if modifier is not Qt.KeyboardModifier.NoModifier:
            match modifier:
                case Qt.KeyboardModifier.ControlModifier:
                    return Keystroke(
                        key=key.name,
                        scan_code=scan_code,
                        modifier=ModifierKey("CTRL", CTRL),
                    )

                case Qt.KeyboardModifier.AltModifier:
                    return Keystroke(
                        key=key.name,
                        scan_code=scan_code,
                        modifier=ModifierKey("ALT", ALT),
                    )
                case _:
                    pass
        return Keystroke(
            key=key.name,
            scan_code=scan_code,
        )
    except ValueError:
        logger.error(f"Invalid key event: {event}")
    except Exception as e:
        logger.error(f"Error matching key event: {e}")
