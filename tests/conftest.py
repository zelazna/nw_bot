from pathlib import Path
from unittest.mock import Mock

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
def res_folder():
    return RES_FOLDER


@pytest.fixture
def config_file_path(res_folder):
    return res_folder / "nwbot_config.txt"


@pytest.fixture
def config_file(config_file_path):
    with open(config_file_path) as fp:
        return fp.read()


@pytest.fixture
def stroke_factory():
    def create(
        *,
        key="Key_5",
        vk=0,
        modifier=ModifierKey(key="Shift", vk=160),
    ):
        Keystroke.controller = Mock(spec=KeyController)
        return Keystroke(
            key,
            vk,
            modifier,
        )

    return create


@pytest.fixture
def click_factory():
    def create(*, kind=Button.left, pos=(0, 0)):
        MouseClick.controller = Mock(spec=MouseController)
        return MouseClick(kind, pos)

    return create


@pytest.fixture
def directional_key_factory():
    def create(*, key="Up"):
        DirectionalKeystroke.controller = Mock(spec=KeyController)
        return DirectionalKeystroke(key)

    return create


@pytest.fixture
def params_factory(stroke_factory, click_factory, directional_key_factory):
    def _create(
        limit: float = 0.01,
        winNum: int = 1,
        interval: str = "1-2",
        num_keystrokes: int = 1,
        num_mouse_click: int = 1,
    ):
        commands = []
        for _ in range(1, num_keystrokes + 1):
            commands.append(stroke_factory())
        for _ in range(1, num_mouse_click + 1):
            commands.append(click_factory())

        commands.append(directional_key_factory())

        return Params(
            limit=limit,  # type: ignore
            commands=commands,
            winNum=winNum,
            interval=interval,
        )

    return _create
