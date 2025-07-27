from typing import Callable
from unittest.mock import call, patch

from bot.core import Keystroke
from bot.core.control import keystroke, mouseClick, run
from bot.models import MouseClick, Params


def test_keystroke(stroke_factory: Callable[[], Keystroke]):
    with (
        patch("bot.core.control.keyboard.press") as mock_press,
        patch("bot.core.control.keyboard.release") as mock_release,
    ):
        stroke = stroke_factory()
        keystroke(stroke, 0)
        assert mock_press.call_args_list == [
            call(stroke.modifier.key_code),  # type: ignore
            call(stroke.key_code),
        ]
        assert mock_release.call_args_list == [
            call(stroke.key_code),
            call(stroke.modifier.key_code),  # type: ignore
        ]


def test_mouse_click(click_factory: Callable[[], MouseClick]):
    with (
        patch("bot.core.control.mouse.press") as mock_press,
        patch("bot.core.control.mouse.release") as mock_release,
    ):
        click = click_factory()
        mouseClick(click, 0)
        assert mock_press.call_args_list == [call(click.kind)]
        assert mock_release.call_args_list == [call(click.kind)]


def test_run(params_factory: Callable[[], Params]):
    p = params_factory()
    stroke, click = p.commands[0], p.commands[1]
    with (
        patch("bot.core.control.keystroke") as k_press,
        patch("bot.core.control.mouseClick") as m_click,
        patch("bot.core.control.time.sleep") as sleep,
    ):
        run(params_factory())
        assert k_press.call_args_list[0] == call(stroke)
        assert m_click.call_args_list[0] == call(click)
        assert sleep.call_args_list[0] == call(5)
