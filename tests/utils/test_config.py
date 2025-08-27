import logging
import os
import tempfile
from pathlib import Path

import pytest

from bot.core.constants import APP_NAME
from bot.models import Button, DirectionalKeystroke, Keystroke, MouseClick, Params
from bot.utils.config import loadConfig, saveConfig


def test_load_config(config_file_path, caplog):
    result = loadConfig(config_file_path)
    assert isinstance(result, Params)
    assert result.winNum == 2
    assert result.limit == 4.0
    assert result.interval == "1-3"
    keystroke, a, mouseclick, directional, special, *_ = result.commands

    assert isinstance(mouseclick, MouseClick)
    assert mouseclick.kind == Button.left
    assert mouseclick.pos == (156, 251)

    assert isinstance(keystroke, Keystroke)
    assert repr(keystroke) == "Shift+5 5000"
    assert keystroke.hold.seconds == 5

    assert repr(a) == "A 200"

    assert isinstance(directional, DirectionalKeystroke)
    assert directional.key == "up"

    assert repr(special) == "Esc 200"
    assert caplog.record_tuples == [
        (APP_NAME, logging.WARNING, "Unhandled command line: 'Oopsie'")
    ]


@pytest.mark.parametrize(
    ("file_name", "lenght"),
    [("test_1.txt", 15), ("test_2.txt", 11), ("test_3.txt", 11)],
)
def test_load_all_keys(res_folder, file_name, lenght):
    result = loadConfig(res_folder / file_name)
    assert isinstance(result, Params)
    assert len(result.commands) == lenght


def test_save_config(params_factory):
    with tempfile.TemporaryDirectory() as tmpdirname:
        filePath = os.path.join(tmpdirname, "test.txt")
        saveConfig(filePath, params_factory())
        assert Path(filePath).exists()
        with open(filePath) as f:
            data = f.read()
        assert data == (
            """winNum 1
limit 1
interval 1-2

Shift+5 200
Left Click: (0, 0)
Up 200

"""
        )
