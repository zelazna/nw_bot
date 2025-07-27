from unittest.mock import call, patch

from pynput.mouse import Button

from bot.core import Keystroke
from bot.core.control import keystroke, mouseClick, run
from bot.models import ModifierKey, MouseClick, Params


def test_keystroke():
    with (
        patch("bot.core.control.keyboard.press") as mock_press,
        patch("bot.core.control.keyboard.release") as mock_release,
    ):
        stroke = Keystroke(key="Key_5", vk=0, modifier=ModifierKey(key="Shift", vk=160))
        keystroke(stroke, 0)
        assert mock_press.call_args_list == [
            call(stroke.modifier.key_code),  # type: ignore
            call(stroke.key_code),
        ]
        assert mock_release.call_args_list == [
            call(stroke.key_code),
            call(stroke.modifier.key_code),  # type: ignore
        ]


def test_mouse_click():
    with (
        patch("bot.core.control.mouse.press") as mock_press,
        patch("bot.core.control.mouse.release") as mock_release,
    ):
        click = MouseClick(kind=Button.left, pos=(0, 0))
        mouseClick(click, 0)
        assert mock_press.call_args_list == [call(click.kind)]
        assert mock_release.call_args_list == [call(click.kind)]


def test_run():
    stroke = Keystroke(key="Key_5", vk=0, modifier=ModifierKey(key="Shift", vk=160))
    click = MouseClick(kind=Button.left, pos=(0, 0))
    params = Params(limit=0.01, commands=[stroke, click], winNum=1, interval="1-2")
    with (
        patch("bot.core.control.keystroke") as k_press,
        patch("bot.core.control.mouseClick") as m_click,
        patch("bot.core.control.time.sleep") as sleep,
    ):
        run(params)
        assert k_press.call_args_list[0] == call(stroke)
        assert m_click.call_args_list[0] == call(click)
        assert sleep.call_args_list[0] == call(5)
