from bot.utils import format_time


def test_format_time():
    assert format_time(5**10) == "02:42:45"
