import logging
from unittest.mock import patch

from bot.core.constants import APP_NAME
from bot.core.control import run


def test_run(params_factory, key_controller, signals):
    p = params_factory(winNum=2, interval="1")
    with (
        patch("bot.core.control.time") as time,
        patch("bot.models.timer.time") as timer_time,
        patch("bot.core.control.alt_tab") as alt_tab,
    ):
        time.time.side_effect = [1, 1, 99]
        run(p, signals)
        timer_time.sleep.assert_any_call(5.0)
        timer_time.sleep.assert_called_with(1)
        key_controller.pressed.assert_called()
        alt_tab.execute.assert_called()


def test_run_on_command_indices(params_factory, signals):
    collected: list[int] = []
    p = params_factory(winNum=1, interval="1")
    signals.current_command.emit.side_effect = collected.append
    with (
        patch("bot.core.control.time") as time,
        patch("bot.models.timer.time"),
    ):
        time.time.side_effect = [1, 1, 99]
        run(p, signals)

    expected = [i for i, cmd in enumerate(p.commands) if cmd.is_reportable]
    assert collected == expected


def test_run_error(params_factory, caplog, stroke_factory, key_controller, signals):
    cmd = stroke_factory()
    key_controller.pressed.side_effect = TypeError
    p = params_factory(commands=(cmd,))
    with (
        patch("bot.core.control.time") as time,
        patch("bot.models.timer.time"),
    ):
        time.time.side_effect = [1, 1, 99]
        run(p, signals)
    assert caplog.record_tuples[3] == (
        APP_NAME,
        logging.ERROR,
        f"Command {cmd!r} not handled skipping",
    )
