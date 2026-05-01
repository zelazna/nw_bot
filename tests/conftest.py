from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest
from pynput.keyboard import Controller as KeyController
from pynput.mouse import Controller as MouseController

from bot.models import (
    Button,
    DirectionalKeystroke,
    Keystroke,
    ModifierKey,
    MouseClick,
    Params,
)

CURRENT_FOLDER = Path(__file__).parent
RES_FOLDER = CURRENT_FOLDER / "res"


@pytest.fixture
def signals():
    return MagicMock()


@pytest.fixture
def res_folder():
    return RES_FOLDER


@pytest.fixture
def config_file_path(res_folder):
    return res_folder / "test.json"


@pytest.fixture
def config_file(config_file_path):
    with open(config_file_path) as fp:
        return fp.read()


@pytest.fixture
def key_controller():
    k_ctlr = Mock(spec=KeyController)
    k_ctlr.pressed.return_value = MagicMock()

    return k_ctlr


@pytest.fixture
def mouse_controller():
    return Mock(spec=MouseController)


@pytest.fixture
def modifier_factory(key_controller, monkeypatch):
    monkeypatch.setattr("bot.models.keyboard._default_keyboard_executor", key_controller)

    def create(*, key="Shift", vk=160):
        return ModifierKey(key=key, vk=vk)

    return create


@pytest.fixture
def stroke_factory(key_controller, modifier_factory, monkeypatch):
    monkeypatch.setattr("bot.models.keyboard._default_keyboard_executor", key_controller)

    def create(
        *,
        key="Key_5",
        vk=0,
        modifier=None,
    ):
        return Keystroke(
            key=key,
            vk=vk,
            modifier=modifier or modifier_factory(),
        )

    return create


@pytest.fixture
def click_factory(mouse_controller, monkeypatch):
    monkeypatch.setattr("bot.models.mouse._default_mouse_executor", mouse_controller)

    def create(*, kind=Button.left, pos=(0, 0)):
        return MouseClick(kind=kind, pos=pos)

    return create


@pytest.fixture
def directional_key_factory(key_controller, monkeypatch):
    monkeypatch.setattr("bot.models.keyboard._default_keyboard_executor", key_controller)

    def create(*, key="Up"):
        return DirectionalKeystroke(key=key)

    return create


@pytest.fixture
def params_factory(stroke_factory, click_factory, directional_key_factory):
    def _create(
        limit=1,
        winNum=1,
        interval="1-2",
        commands=None,
    ):
        return Params(
            limit=limit,
            commands=commands
            or tuple([stroke_factory(), click_factory(), directional_key_factory()]),
            winNum=winNum,
            interval=interval,
        )

    return _create
