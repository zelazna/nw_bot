import re
from functools import lru_cache
from pathlib import Path

from pynput.keyboard import Key, KeyCode

from bot.models import (
    Button,
    DirectionalKeystroke,
    Keystroke,
    ModifierKey,
    MouseClick,
    Params,
    Timer,
    directionalMapping,
)
from bot.models.command import Command
from bot.utils.logger import logger

directional = [k.name for k in directionalMapping.values()]
time_pattern = r"^.* (\d{2}):(\d{2})$"


@lru_cache(maxsize=25)
def parse_commands(line: str) -> Command | None:
    timer = Timer(200)

    if founds := re.findall(r"\w+\s(\d{2,4})", line):
        timer = Timer(int(founds[0]))

    # Click
    if match := re.match(r"(Left|Right) Click: \((\d+),\s*(\d+)\)", line):
        side, x, y = match.groups()
        kind = Button.left if side == "Left" else Button.right
        return MouseClick(kind=kind, pos=(int(x), int(y)))

    # Key with modifier
    elif match := re.match(r"(\w.*)\+(\w)", line):
        modifier, key = match.groups()
        code = KeyCode.from_char(key)
        mod = ModifierKey(modifier, getattr(Key, modifier.lower()).value.vk)
        return Keystroke(key, code.vk, mod, hold=timer)

    # Directional keys
    elif match := re.match(r"^(Up|Down|Left|Right)(?!\s+Click)", line):
        key = match.group()
        return DirectionalKeystroke(key.lower(), hold=timer)

    # Special keys
    elif match := re.match(r"^(Esc|Enter|Return|Space)", line):
        key = match.group().lower()
        k = getattr(Key, match.group().lower())
        return Keystroke(key, k.value.vk or 0, hold=timer)

    # Single normal keys
    elif match := re.match(r"^(.)\s\d+$", line):
        key = match.groups()[0].lower()
        code = KeyCode.from_char(key)
        return Keystroke(key, code.vk, hold=timer)

    else:
        logger.warning(f"Unhandled Key {line}")


def loadConfig(filename: str | Path) -> Params | None:
    with open(filename, "r", encoding="utf-8") as fp:
        lines = [line.strip() for line in fp if line.strip()]
        win_num = int(lines[0].split()[1])
        limit = int(lines[1].split()[1])
        interval = lines[2].split()[1]

    return Params(
        winNum=win_num,
        limit=limit,
        interval=interval,
        commands=[c for line in lines[3:] if (c := parse_commands(line))],
    )


def saveConfig(filePath: str | Path, params: Params):
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(repr(params))
