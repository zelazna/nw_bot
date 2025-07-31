from typing import cast
import pytest
from pynput.keyboard import Key
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent

from bot.core.keystroke_adapter import CTRL_VK, match
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


def test_unhandled_modifier():
    event = QKeyEvent(QEvent.Type.KeyRelease, 0x35, Qt.KeyboardModifier.MetaModifier)
    result = match(event)
    assert isinstance(result, Keystroke)
    assert result.modifier is None


def test_match_nothing():
    event = QKeyEvent(
        QEvent.Type.KeyRelease, 16777249, Qt.KeyboardModifier.NoModifier, 29, CTRL_VK, 0
    )
    assert match(event) is None


def test_with_directionnal():
    event = QKeyEvent(
        QEvent.Type.KeyRelease,
        16777249,
        Qt.KeyboardModifier.NoModifier,
        29,
        cast(int, Key.up.value.vk),
        0,
    )
    result = match(event)
    assert isinstance(result, Keystroke)
