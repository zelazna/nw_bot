import re
from functools import lru_cache
from pathlib import Path

from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button

from bot.core.keystroke_adapter import directionalMapping
from bot.models import (
    DirectionalKeystroke,
    Keystroke,
    ModifierKey,
    MouseClick,
    Params,
    Timer,
)
from bot.utils.logger import logger

directional = [k.name for k in directionalMapping.values()]

pos_pattern = r"\((\d+),\s(\d+)\)"
time_pattern = r"^.* (\d{2}):(\d{2})$"


def loadConfig(filename: str | Path) -> Params:
    commands = []
    with open(filename, "r", encoding="utf-8") as fp:
        for k in fp:
            k = k[:-1]  # remove line break
            if "Click" in k:
                x, y = 0, 0
                kind, _, pos = k.split(" ", 2)
                button = getattr(Button, kind.lower())
                match = re.search(pos_pattern, pos)
                if match:
                    x, y = int(match.group(1)), int(match.group(2))
                commands.append(MouseClick(button, (x, y)))
            else:
                splited = k.split(" ")
                if len(splited) == 1:
                    key = splited[0]
                    timer = Timer(200)
                else:
                    key, time = splited
                    timer = Timer(int(time))

                if "+" in key:
                    modifier, key = key.split("+")
                    code = KeyCode.from_char(key)
                    if modifier_key := getattr(Key, modifier.lower()):
                        mod = ModifierKey(modifier, modifier_key.value.vk)
                        commands.append(Keystroke(key, code.vk or 0, mod, hold=timer))
                    logger.warning(f"couldn't parse {k}")
                elif key.lower() in directional:
                    commands.append(DirectionalKeystroke(key.lower(), hold=timer))
                else:
                    code = KeyCode.from_char(key)
                    if not code.vk:
                        logger.warning(f"No vk found for {k}")
                    commands.append(Keystroke(key, code.vk or 0, hold=timer))

    return Params(commands)


def saveConfig(filePath: str | Path, params: Params):
    with open(filePath, "w", encoding="utf-8") as f:
        f.writelines([f"{cmd!r}\n" for cmd in params.commands])
