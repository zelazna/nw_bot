from unittest.mock import call, patch

from pynput.keyboard import KeyCode, Key
from pynput.mouse import Button

from bot.models import Keystroke, Params


def test_keystroke(stroke_factory):
    model = stroke_factory()
    assert repr(model) == "Shift+5 200"
    assert model.modifier.key_code == KeyCode(model.modifier.vk)
    with patch("bot.models.timer.time.sleep") as sleep:
        model.execute()
        assert model.controller.press.call_args_list == [
            call(model.modifier.key_code),
            call(model.key_code),
        ]
        assert model.controller.release.call_args_list == [
            call(model.key_code),
            call(model.modifier.key_code),
        ]
        sleep.assert_called_once_with(model.hold.seconds)
        assert repr(Keystroke("truc", 125)) == "Truc 200"


def test_directional(directional_key_factory):
    model = directional_key_factory()
    key = getattr(Key, model.key.lower())
    with patch("bot.models.timer.time.sleep") as sleep:
        model.execute()
        model.controller.press.assert_called_once_with(key)
        model.controller.release.assert_called_once_with(key)
        sleep.assert_called_once_with(model.hold.seconds)


def test_params(stroke_factory):
    model = Params(limit=5, commands=[stroke_factory()], winNum=1, interval="1-5")
    assert model.interval_range == [1, 2, 3, 4, 5]
    model.interval = "1"
    assert model.interval_range == [1]
    assert repr(model) == "winNum 1\nlimit 5\ninterval 1\n\nShift+5 200\n\n"


def test_mouse_click(click_factory):
    model = click_factory()
    assert repr(model) == "Left Click: (0, 0)"
    button = getattr(Button, model.kind.name)
    model.execute()
    model.controller.press.assert_called_once_with(button)
    model.controller.release.assert_called_once_with(button)
