from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from bot.core.constants import ALT, CTRL, INVERTED_KEYMAP, KEYMAP
from bot.models import Keystroke, ModifierKey

ALT_TAB = Keystroke(
    key="TAB", scan_code=KEYMAP["TAB"], modifier=ModifierKey("ALT", 0x38)
)


def match(event: QKeyEvent) -> Keystroke | None:
    modifier = event.modifiers()
    scan_code = event.nativeScanCode()
    key = INVERTED_KEYMAP.get(scan_code, None)

    if scan_code in (CTRL, ALT):
        # Ignore CTRL and ALT keys as they are modifiers
        return None

    # Handle direction keys
    maybe_directional = event.key()
    match maybe_directional:
        case Qt.Key.Key_Up.value:
            return Keystroke(
                key="KEY_UP",
                scan_code=scan_code,
            )
        case Qt.Key.Key_Down.value:
            return Keystroke(
                key="KEY_DOWN",
                scan_code=scan_code,
            )
        case Qt.Key.Key_Left.value:
            return Keystroke(
                key="KEY_LEFT",
                scan_code=scan_code,
            )
        case Qt.Key.Key_Right.value:
            return Keystroke(
                key="KEY_RIGHT",
                scan_code=scan_code,
            )
        case Qt.Key.Key_Down.value:
            return Keystroke(
                key="KEY_DOWN",
                scan_code=scan_code,
            )
        case _:
            pass

    if key is not None:
        if modifier is not Qt.KeyboardModifier.NoModifier:
            match modifier:
                case Qt.KeyboardModifier.ControlModifier:
                    return Keystroke(
                        key=key,
                        scan_code=scan_code,
                        modifier=ModifierKey("CTRL", KEYMAP["CTRL"]),
                    )

                case Qt.KeyboardModifier.AltModifier:
                    return Keystroke(
                        key=key,
                        scan_code=scan_code,
                        modifier=ModifierKey("ALT", KEYMAP["ALT"]),
                    )
                case _:
                    pass

        return Keystroke(
            key=INVERTED_KEYMAP[scan_code],
            scan_code=scan_code,
        )
