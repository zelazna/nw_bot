import json
import os
from typing import Any
from bot.models import KeysModel
from bot.core.keystroke_adapter import Keystroke, ModifierKey, encode_value


def load_config(filename: str, model: KeysModel) -> dict[str, Any]:
    with open(filename, "r") as f:
        config = json.load(f)

        for key in config["keys"]:
            if modifier := key.get("modifier", {}):
                model.keys.append(
                    Keystroke(**{**key, "modifier": ModifierKey(**modifier)})  # type: ignore
                )
            else:
                model.keys.append(Keystroke(**key))
        return config


def save_config(filename: str, folder: str, config: dict[str, Any]):
    filepath = os.path.join(folder, filename)
    with open(filepath, "w") as f:
        return json.dump(config, f, indent=4, default=encode_value)
