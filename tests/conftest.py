from pathlib import Path
from typing import Any, Callable

import pytest
from pynput.mouse import Button

from bot.core import Keystroke
from bot.models import ModifierKey, MouseClick, Params

CURRENT_FOLDER = Path(__file__).parent
RES_FOLDER = CURRENT_FOLDER / "res"


@pytest.fixture
def res_folder() -> Path:
    return RES_FOLDER


@pytest.fixture
def config_file_path(res_folder: Path) -> Path:
    return res_folder / "nwbot_config.json"


@pytest.fixture
def config_file(config_file_path: Path) -> str:
    with open(config_file_path) as fp:
        return fp.read()


@pytest.fixture
def stroke_factory() -> Callable[[], Keystroke]:
    def create(
        *,
        key: str = "Key_5",
        vk: int = 0,
        modifier: ModifierKey = ModifierKey(key="Shift", vk=160),
    ):
        return Keystroke(key=key, vk=vk, modifier=modifier)

    return create


@pytest.fixture
def click_factory() -> Callable[[], MouseClick]:
    def create(*, kind: Button = Button.left, pos: tuple[int, int] = (0, 0)):
        return MouseClick(kind=kind, pos=pos)

    return create


@pytest.fixture
def params_factory(
    stroke_factory: Callable[[], Keystroke],
    click_factory: Callable[[], MouseClick],
) -> Callable[[Any], Params]:
    def _create(
        limit: float = 0.01,
        winNum: int = 1,
        interval: str = "1-2",
        num_keystrokes: int = 1,
        num_mouse_click: int = 1,
    ):
        commands: list[Keystroke | MouseClick] = []
        for _ in range(1, num_keystrokes + 1):
            commands.append(stroke_factory())
        for _ in range(1, num_mouse_click + 1):
            commands.append(click_factory())

        return Params(
            limit=limit,
            commands=commands,
            winNum=winNum,
            interval=interval,
        )

    return _create
