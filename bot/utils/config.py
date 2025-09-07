import json
from bot.models import Params


def loadConfig(filename: str) -> Params:
    with open(filename, "r", encoding="utf-8") as fp:
        return Params.model_validate_json(fp.read())


def saveConfig(filePath: str, params: Params):
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(
            json.dumps(
                params.model_dump(mode="json"),
                indent=4,
                sort_keys=True,
            )
        )
