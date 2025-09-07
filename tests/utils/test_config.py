import json
import os
import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from bot.models import Button, DirectionalKeystroke, Keystroke, MouseClick, Params
from bot.utils.config import loadConfig, saveConfig


def test_load_config(config_file_path):
    result = loadConfig(config_file_path)
    assert isinstance(result, Params)
    assert result.winNum == 2
    assert result.limit == 4
    assert result.interval == "1-3"
    keystroke, a, mouseclick, directional, special, *_ = result.commands

    assert isinstance(mouseclick, MouseClick)
    assert mouseclick.kind == Button.left
    assert mouseclick.pos == (338, 260)

    assert isinstance(keystroke, Keystroke)
    assert repr(keystroke) == "Shift+PERCENT 5000"
    assert keystroke.hold.seconds == 5

    assert repr(a) == "A 200"

    assert isinstance(directional, DirectionalKeystroke)
    assert directional.key == "up"

    assert repr(special) == "Escape 200"


def test_save_config(params_factory):
    with tempfile.TemporaryDirectory() as tmpdirname:
        filePath = os.path.join(tmpdirname, "test.json")
        saveConfig(filePath, params_factory())
        assert Path(filePath).exists()
        with open(filePath) as f:
            data = json.load(f)
        assert data == {
            "commands": [
                {
                    "key": "Key_5",
                    "vk": 0,
                    "hold": {"milliseconds": 200},
                    "modifier": {
                        "key": "Shift",
                        "vk": 160,
                        "hold": {"milliseconds": 200},
                    },
                },
                {"kind": 1, "pos": [0, 0]},
                {
                    "key": "Up",
                    "vk": None,
                    "hold": {"milliseconds": 200},
                    "is_directional": True,
                },
            ],
            "winNum": 1,
            "limit": 1,
            "interval": "1-2",
        }


def test_load_config_with_malformed_json(tmp_path):
    malformed_json = "{ invalid json: true, }"
    tmp = tmp_path / "test.json"
    tmp.write_text(malformed_json)

    with pytest.raises(ValidationError) as exc:
        loadConfig(str(tmp))
    assert "Invalid JSON" in str(exc.value)
