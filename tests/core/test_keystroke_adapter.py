import logging
from typing import cast
from unittest.mock import Mock

import pytest
from pynput.keyboard import Key, KeyCode
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent

from bot.core.keystroke_adapter import (
    CTRL_VK,
    PynputKeystrokeAdapter,
    QtKeystrokeAdapter,
)
from bot.models import (
    CommandListModel,
    DirectionalKeystroke,
    Keystroke,
    ModifierKey,
)


@pytest.fixture
def qt_adapter():
    model = CommandListModel()
    model.layoutChanged = Mock()  # type: ignore
    adapter = QtKeystrokeAdapter(model)
    return adapter


@pytest.fixture
def pynput_adapter():
    model = CommandListModel()
    model.layoutChanged = Mock()  # type: ignore
    adapter = PynputKeystrokeAdapter(model)
    return adapter


def test_key_release(qt_adapter):
    event = QKeyEvent(QEvent.Type.KeyRelease, 0x35, Qt.KeyboardModifier.NoModifier)
    qt_adapter.on_key_release(event)
    result = qt_adapter.model.commands[0]
    assert isinstance(result, Keystroke)
    assert result.key == "Key_5"
    assert result.modifier is None
    assert result.vk == 0
    qt_adapter.model.layoutChanged.emit.assert_called_once()


events = [
    (
        "Alt",
        "Alt+5 200",
        18,
        QKeyEvent(QEvent.Type.KeyRelease, 0x35, Qt.KeyboardModifier.AltModifier),
    ),
    (
        "Ctrl",
        "Ctrl+5 200",
        17,
        QKeyEvent(QEvent.Type.KeyRelease, 0x35, Qt.KeyboardModifier.ControlModifier),
    ),
    (
        "Shift",
        "Shift+5 200",
        160,
        QKeyEvent(QEvent.Type.KeyRelease, 0x35, Qt.KeyboardModifier.ShiftModifier),
    ),
]


@pytest.mark.parametrize(("key", "rep", "vk", "event"), events)
def test_on_key_release_with_modifier(key, rep, vk, event, qt_adapter):
    qt_adapter.on_key_release(event)
    assert qt_adapter.model.rowCount() == 1
    result = qt_adapter.model.commands[0]
    assert isinstance(result, Keystroke)
    assert isinstance(result.modifier, ModifierKey)
    assert result.modifier.key == key
    assert result.modifier.vk == vk
    assert repr(result) == rep


def test_unhandled_modifier(qt_adapter):
    event = QKeyEvent(QEvent.Type.KeyRelease, 0x35, Qt.KeyboardModifier.MetaModifier)
    qt_adapter.on_key_release(event)
    result = qt_adapter.model.commands[0]
    assert qt_adapter.model.rowCount() == 1
    assert isinstance(result, Keystroke)
    assert result.modifier is None


def test_match_nothing(qt_adapter):
    event = QKeyEvent(
        QEvent.Type.KeyRelease, 16777249, Qt.KeyboardModifier.NoModifier, 29, CTRL_VK, 0
    )
    qt_adapter.on_key_release(event)
    assert qt_adapter.model.rowCount() == 0


def test_with_directionnal(qt_adapter):
    event = QKeyEvent(
        QEvent.Type.KeyRelease,
        16777249,
        Qt.KeyboardModifier.NoModifier,
        29,
        cast(int, Key.up.value.vk),
        0,
    )
    qt_adapter.on_key_release(event)
    result = qt_adapter.model.commands[0]
    assert qt_adapter.model.rowCount() == 1
    assert isinstance(result, DirectionalKeystroke)
    qt_adapter.model.layoutChanged.emit.assert_called_once()


@pytest.mark.parametrize(
    ("rep", "key", "mod"),
    [
        ("Ctrl+A 0", "\x01", Key.ctrl),
        ("Ctrl+A 0", "a", Key.ctrl),
        ("Shift+Z 0", "z", Key.shift),
        ("Alt+L 0", "l", Key.alt),
    ],
)
def test_pynput_adapter_with_modifiers(pynput_adapter, rep, key, mod):
    pynput_adapter.modifier = mod
    pynput_adapter.on_key_press(KeyCode.from_char(key))
    pynput_adapter.on_key_release(KeyCode.from_char(key))
    assert pynput_adapter.model.rowCount() == 1
    result = pynput_adapter.model.commands[0]
    assert repr(result) == rep
    assert isinstance(result, Keystroke)
    pynput_adapter.model.layoutChanged.emit.assert_called_once()

    pynput_adapter.on_key_release(mod)
    assert pynput_adapter.modifier is None


@pytest.mark.parametrize(
    ("rep", "key", "model"),
    [
        ("A 0", KeyCode.from_char("a"), Keystroke),
        ("Up 0", Key.up, DirectionalKeystroke),
    ],
)
def test_pynput_adapter_without_modifier(pynput_adapter, rep, key, model):
    pynput_adapter.on_key_press(key)
    pynput_adapter.on_key_release(key)
    assert pynput_adapter.model.rowCount() == 1
    result = pynput_adapter.model.commands[0]
    assert repr(result) == rep
    assert isinstance(result, model)
    pynput_adapter.model.layoutChanged.emit.assert_called_once()


def test_pynput_adapter_errors(pynput_adapter, caplog):
    pynput_adapter.modifier = Key.alt
    pynput_adapter.on_key_release(Key.tab)
    assert caplog.record_tuples == [
        (
            "bot.utils.logger",
            logging.ERROR,
            "Unhandled key: <Key.tab: <9>>",
        )
    ]


def test_pynput_adapter_keypress_modifier(pynput_adapter, caplog):
    caplog.set_level(logging.DEBUG)
    pynput_adapter.on_key_press(Key.ctrl)
    assert pynput_adapter.modifier is Key.ctrl
    assert caplog.record_tuples == [
        (
            "bot.utils.logger",
            logging.DEBUG,
            "got modifier key: <Key.ctrl: <17>> ignoring it for know",
        )
    ]


def test_pynput_adapter_with_none(pynput_adapter):
    pynput_adapter.on_key_press(None)
    pynput_adapter.model.layoutChanged.emit.assert_not_called()
