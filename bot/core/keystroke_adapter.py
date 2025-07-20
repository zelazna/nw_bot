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
