from bot.models import Keystroke, MouseClick, Params
from pynput.mouse import Button


def test_keystroke():
    model = Keystroke(key="123", vk=123)
    assert repr(model) == "123"
    assert model.key_code.vk == 123


def test_params():
    model = Params(limit=5, commands=[], winNum=1, interval="1-5")
    assert model.interval_range == [1, 2, 3, 4, 5]
    model.interval = "1"
    assert model.interval_range == [1]


def test_mouse_click():
    model = MouseClick(kind=Button.left, pos=(0, 0))
    assert repr(model) == "Left Click: (0, 0)"