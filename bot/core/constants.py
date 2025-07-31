import importlib.metadata
from typing import cast

from pynput.keyboard import Key

VERSION = importlib.metadata.version("nw-bot")
LOG_FILE = "nw-bot.log"
MIME_TYPE = "application/vnd.text.list"
PADDING_IN_S = 5
TIMER_TIMEOUT_MILLISEC = 500

ALT_VK = cast(int, Key.alt.value.vk)
TAB_VK = cast(int, Key.tab.value.vk)
CTRL_VK = cast(int, Key.ctrl.value.vk)
SHIFT_VK = cast(int, Key.shift.value.vk)
DEL_VK = cast(int, Key.delete.value.vk)