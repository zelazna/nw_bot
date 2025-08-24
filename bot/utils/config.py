import re
from functools import lru_cache

from pynput.keyboard import Key, KeyCode
from bot.models import (
    Button,
    DirectionalKeystroke,
    Keystroke,
    ModifierKey,
    MouseClick,
    Params,
    Timer,
)
from bot.models.command import Command
from bot.utils.logger import logger

CLICK_RE = re.compile(r"(Left|Right) Click: \((\d+),\s*(\d+)\)")
MODIFIER_RE = re.compile(r"(\w+)\+(\w)")
DIRECTION_RE = re.compile(r"^(Up|Down|Left|Right)")
SPECIAL_RE = re.compile(r"^(Esc|Enter|Return|Space)")
NORMAL_RE = re.compile(r"^(.)\s\d+$")
TIMER_RE = re.compile(r"\w+\s(\d{2,4})")


def _make_keystroke(
    key: str, hold: Timer, modifier: ModifierKey | None = None
) -> Keystroke:
    code = KeyCode.from_char(key)
    return Keystroke(key, code.vk, modifier, hold=hold)


@lru_cache
def parse_commands(line: str) -> Command | None:
    timer = Timer(200)

    if founds := TIMER_RE.findall(line):
        timer = Timer(int(founds[0]))

    if match := CLICK_RE.match(line):
        side, x, y = match.groups()
        kind = Button.left if side == "Left" else Button.right
        return MouseClick(kind=kind, pos=(int(x), int(y)))

    elif match := MODIFIER_RE.match(line):
        modifier, key = match.groups()
        mod = ModifierKey(modifier, getattr(Key, modifier.lower()).value.vk)
        return _make_keystroke(key, timer, mod)

    elif match := DIRECTION_RE.match(line):
        return DirectionalKeystroke(match.group().lower(), hold=timer)

    elif match := SPECIAL_RE.match(line):
        key = match.group().lower()
        k: Key = getattr(Key, key)
        return Keystroke(key, k.value.vk or 0, hold=timer)

    elif match := NORMAL_RE.match(line):
        return _make_keystroke(match.group(1).lower(), timer)

    logger.warning(f"Unhandled command line: '{line}'")
    return None


def loadConfig(filename: str) -> Params | None:
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


def saveConfig(filePath: str, params: Params):
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(repr(params))
