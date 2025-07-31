from pathlib import Path

from bot.models import Params


def loadConfig(filename: str | Path) -> Params:
    with open(filename, "r") as f:
        ...
        # return Params.model_validate_json(f.read())


def saveConfig(filePath: str | Path, params: Params):
    with open(filePath, "w") as f:
        ...
        # f.write(params.model_dump_json())
