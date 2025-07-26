import dataclasses
import datetime
import functools
import json
import os
from typing import Any

from bot.models import CommandsModel, Keystroke, ModifierKey, Params


@functools.singledispatch
def encode_value(x: Any) -> Any:
    if dataclasses.is_dataclass(x):
        return dataclasses.asdict(x)  # type: ignore
    elif isinstance(x, datetime.datetime):
        return x.isoformat()
    return x


def load_config(filename: str, model: CommandsModel) -> dict[str, Any]:
    with open(filename, "r") as f:
        config = json.load(f)

        for key in config["keys"]:
            if modifier := key.get("modifier", {}):
                model.commands.append(
                    Keystroke(**{**key, "modifier": ModifierKey(**modifier)})  # type: ignore
                )
            else:
                model.commands.append(Keystroke(**key))
        return config


def save_config(filename: str, folder: str, config: Params):
    filepath = os.path.join(folder, filename)
    with open(filepath, "w") as f:
        json.dump(config, f, indent=4, default=encode_value)
