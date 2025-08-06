from functools import lru_cache
import re
from pathlib import Path

from pynput.keyboard import Key, KeyCode

from bot.core.keystroke_adapter import directionalMapping
from bot.models import (
    DirectionalKeystroke,
    Keystroke,
    ModifierKey,
    MouseClick,
    Params,
    Timer,
    Button,
)
from bot.models.base_command import BaseCommand
from bot.utils.logger import logger

directional = [k.name for k in directionalMapping.values()]
time_pattern = r"^.* (\d{2}):(\d{2})$"


@lru_cache(maxsize=25)
def parse_commands(line: str) -> BaseCommand | None:
    if match := re.match(r"(Left|Right) Click: \((\d+),\s*(\d+)\)", line):
        side, x, y = match.groups()
        kind = Button.left if side == "Left" else Button.right
        return MouseClick(kind=kind, pos=(int(x), int(y)))
    else:
        splited = line.split(" ")
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
                return Keystroke(key, code.vk or 0, mod, hold=timer)
            logger.warning(f"couldn't parse {line}")
            return None
        elif key.lower() in directional:
            return DirectionalKeystroke(key.lower(), hold=timer)
        else:
            code = KeyCode.from_char(key)
            if not code.vk:
                logger.warning(f"No vk found for {line}")
            return Keystroke(key, code.vk or 0, hold=timer)


@lru_cache(maxsize=10)
def loadConfig(filename: str | Path) -> Params:
    commands = []
    with open(filename, "r", encoding="utf-8") as fp:
        lines = [line.strip() for line in fp if line.strip()]
        win_num = int(lines[0].split()[1])
        limit = float(lines[1].split()[1])
        interval = lines[2].split()[1]

        commands: list[BaseCommand] = []

        for line in lines[3:]:
            if c := parse_commands(line):
                commands.append(c)

    return Params(winNum=win_num, limit=limit, interval=interval, commands=commands)


def saveConfig(filePath: str | Path, params: Params):
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(repr(params))
