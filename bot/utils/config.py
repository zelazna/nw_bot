import os

from bot.models import Params


def load_config(filename: str) -> Params:
    with open(filename, "r") as f:
        return Params.model_validate_json(f.read())


def save_config(filename: str, folder: str, params: Params):
    filepath = os.path.join(folder, filename)
    with open(filepath, "w") as f:
        f.write(params.model_dump_json())
