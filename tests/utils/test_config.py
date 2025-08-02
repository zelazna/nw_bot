import os
import tempfile
from pathlib import Path

from pynput.mouse import Button

from bot.models import MouseClick, Params, Keystroke
from bot.utils import loadConfig, saveConfig


def test_load_config(config_file_path):
    result = loadConfig(config_file_path)
    assert isinstance(result, Params)
    assert result.limit == 5
    assert result.interval == "1"
    keystroke, a, mouseclick, _ = result.commands

    assert isinstance(mouseclick, MouseClick)
    assert mouseclick.kind == Button.left

    assert isinstance(keystroke, Keystroke)
    assert repr(keystroke) == "Shift+5"

    assert repr(a) == "A"


def test_save_config(params_factory):
    with tempfile.TemporaryDirectory() as tmpdirname:
        filePath = os.path.join(tmpdirname, "test.txt")
        saveConfig(filePath, params_factory())
        assert Path(filePath).exists()
        with open(filePath) as f:
            data = f.read()
        assert (
            data
            == """Shift+5
Left Click: (0, 0)
"""
        )
