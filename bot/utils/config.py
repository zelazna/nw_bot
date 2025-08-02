from pathlib import Path

from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button

from bot.models import ModifierKey, MouseClick, Params, Keystroke
from bot.utils.logger import logger
from bot.core.keystroke_adapter import directionalMapping

directional = [k.name for k in directionalMapping.values()]


def loadConfig(filename: str | Path) -> Params:
    commands = []
    with open(filename, "r") as fp:
        for k in fp:
            k = k[:-1]  # remove line break
            if "Click" in k:
                kind, _, _ = k.split(" ", 2)
                button = getattr(Button, kind.lower())
                commands.append(MouseClick(button, (0, 0)))
            else:
                if "+" in k:
                    modifier, key = k.split("+")
                    code = KeyCode.from_char(key)
                    if modifier_key := getattr(Key, modifier.lower()):
                        mod = ModifierKey(modifier, modifier_key.value.vk)
                        commands.append(Keystroke(key, code.vk, mod))
                    logger.warning("couldn't parse {k}")
                elif k.lower() in directional:
                    ...
                else:
                    code = KeyCode.from_char(k)
                    commands.append(Keystroke(k, code.vk))

    return Params(commands)


def saveConfig(filePath: str | Path, params: Params):
    with open(filePath, "w") as f:
        f.writelines([f"{repr(cmd)}\n" for cmd in params.commands])
