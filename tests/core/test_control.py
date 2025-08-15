from unittest.mock import Mock, call, patch

from bot.core.control import run


def test_run(params_factory):
    p = params_factory(winNum=2)
    cmd_mock = Mock()
    p.commands = [cmd_mock]
    with (
        patch("bot.core.control.time.sleep") as sleep,
        patch("bot.core.control.alt_tab") as alt_tab,
    ):
        run(p)
        assert sleep.call_args_list[0] == call(5)
        cmd_mock.execute.assert_called()
        alt_tab.execute.assert_called()
