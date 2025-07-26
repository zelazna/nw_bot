import pytest
from bot.core.KeystrokeAdapter import match

from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt, QEvent

from bot.models import Keystroke, ModifierKey


def test_match():
    event = QKeyEvent(QEvent.Type.KeyRelease, 0x35, Qt.KeyboardModifier.NoModifier)
    result = match(event)
    assert isinstance(result, Keystroke)
    assert result.key == "Key_5"
    assert result.modifier is None
    assert result.vk == 0


events = [
    (
        "Alt",
        "Alt+5",
        18,
        QKeyEvent(QEvent.Type.KeyRelease, 0x35, Qt.KeyboardModifier.AltModifier),
    ),
    (
        "Ctrl",
        "Ctrl+5",
        17,
        QKeyEvent(QEvent.Type.KeyRelease, 0x35, Qt.KeyboardModifier.ControlModifier),
    ),
    (
        "Shift",
        "Shift+5",
        160,
        QKeyEvent(QEvent.Type.KeyRelease, 0x35, Qt.KeyboardModifier.ShiftModifier),
    ),
]


@pytest.mark.parametrize(("key", "rep", "vk", "event"), events)
def test_match_with_modifier(key: str, rep: str, vk: int, event: QKeyEvent):
    result = match(event)
    assert isinstance(result, Keystroke)
    assert isinstance(result.modifier, ModifierKey)
    assert result.modifier.key == key
    assert result.modifier.vk == vk
    assert repr(result) == rep


def match_nothing():
    event = QKeyEvent(QEvent.Type.KeyRelease, 0x1000021, Qt.KeyboardModifier.NoModifier)
    assert match(event) is None
