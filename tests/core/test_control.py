import logging
from unittest.mock import call, patch

from bot.core.constants import APP_NAME
from bot.core.control import run


def test_run(params_factory, key_controller):
    p = params_factory(winNum=2, interval="1")
    with (
        patch("bot.core.control.time") as time,
        patch("bot.core.control.alt_tab") as alt_tab,
    ):
        time.time.side_effect = [1, 1, 99]
        run(p)
        time.sleep.assert_has_calls([call(5), call(1)])
        key_controller.pressed.assert_called()
        alt_tab.execute.assert_called()


def test_run_error(params_factory, caplog, stroke_factory, key_controller):
    cmd = stroke_factory()
    key_controller.pressed.side_effect = TypeError
    p = params_factory(commands=(stroke_factory(),))
    with patch("bot.core.control.time") as time:
        time.time.side_effect = [1, 1, 99]
        run(p)
    assert caplog.record_tuples[2] == (
        APP_NAME,
        logging.ERROR,
        f"Command {cmd!r} not handled skipping",
    )
