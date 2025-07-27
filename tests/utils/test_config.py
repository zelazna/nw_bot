import os
import tempfile
from pathlib import Path
from typing import Callable


from bot.models import Params
from bot.utils import loadConfig, saveConfig


def test_load_config(config_file_path: Path):
    result = loadConfig(config_file_path)
    assert isinstance(result, Params)
    assert result.limit == 2
    assert result.interval == "1-5"


def test_save_config(params_factory: Callable[[], Params]):
    with tempfile.TemporaryDirectory() as tmpdirname:
        filePath = os.path.join(tmpdirname, "test.json")
        saveConfig(filePath, params_factory())
        assert Path(filePath).exists()
