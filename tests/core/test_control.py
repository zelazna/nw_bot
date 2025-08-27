import logging
from unittest.mock import Mock, call, patch

from bot.core.constants import APP_NAME
from bot.core.control import run
from bot.models.command import Command


def test_run(params_factory):
    cmd_mock = Mock(spec=Command)
    p = params_factory(winNum=2, commands=(cmd_mock,), interval="1")
    with (
        patch("bot.core.control.time") as time,
        patch("bot.core.control.alt_tab") as alt_tab,
    ):
        time.time.side_effect = [1, 1, 99]
        run(p)
        time.sleep.assert_has_calls([call(5), call(1)])
        cmd_mock.execute.assert_called()
        alt_tab.execute.assert_called()


def test_run_error(params_factory, caplog):
    cmd_mock = Mock(spec=Command)
    p = params_factory(commands=(cmd_mock,))
    cmd_mock.execute.side_effect = TypeError
    with patch("bot.core.control.time") as time:
        time.time.side_effect = [1, 1, 99]
        run(p)
    assert caplog.record_tuples[2] == (
        APP_NAME,
        logging.ERROR,
        f"Command {cmd_mock!r} not handled skipping",
    )
