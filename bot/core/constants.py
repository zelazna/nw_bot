import importlib.metadata
from typing import cast

from pynput.keyboard import Key

ALT_VK = cast(int, Key.alt.value.vk)
TAB_VK = cast(int, Key.tab.value.vk)
CTRL_VK = cast(int, Key.ctrl.value.vk)
DEL_VK = cast(int, Key.delete.value.vk)
VERSION = importlib.metadata.version("nw-bot")
LOG_FILE = "nw-bot.log"
MIME_TYPE = "application/vnd.text.list"