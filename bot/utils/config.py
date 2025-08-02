import re
from pathlib import Path

from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button

from bot.core.keystroke_adapter import directionalMapping
from bot.models import DirectionalKeystroke, Keystroke, ModifierKey, MouseClick, Params
from bot.utils.logger import logger

directional = [k.name for k in directionalMapping.values()]

pattern = r"\((\d+),\s(\d+)\)"


def loadConfig(filename: str | Path) -> Params:
    commands = []
    with open(filename, "r", encoding="utf-8") as fp:
        for k in fp:
            k = k[:-1]  # remove line break
            if "Click" in k:
                x, y = 0, 0
                kind, _, pos = k.split(" ", 2)
                button = getattr(Button, kind.lower())
                match = re.search(pattern, pos)
                if match:
                    x, y = int(match.group(1)), int(match.group(2))
                commands.append(MouseClick(button, (x, y)))
            else:
                if "+" in k:
                    modifier, key = k.split("+")
                    code = KeyCode.from_char(key)
                    if modifier_key := getattr(Key, modifier.lower()):
                        mod = ModifierKey(modifier, modifier_key.value.vk)
                        commands.append(Keystroke(key, code.vk or 0, mod))
                    logger.warning(f"couldn't parse {k}")
                elif k.lower() in directional:
                    commands.append(DirectionalKeystroke(k.lower()))
                else:
                    code = KeyCode.from_char(k)
                    if not code.vk:
                        logger.warning(f"No vk found for {k}")
                    commands.append(Keystroke(k, code.vk or 0))

    return Params(commands)


def saveConfig(filePath: str | Path, params: Params):
    with open(filePath, "w", encoding="utf-8") as f:
        f.writelines([f"{repr(cmd)}\n" for cmd in params.commands])
