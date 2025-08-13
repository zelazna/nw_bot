import importlib.metadata

from pynput.keyboard import Key

APP_NAME = "NW Bot"
VERSION = importlib.metadata.version("nw-bot")
LOG_FILE = "nw-bot.log"
MIME_TYPE = "application/vnd.text.list"
PADDING_IN_S = 5
TIMER_TIMEOUT_MILLISEC = 500
DEFAULT_CONFIG_FILE = "nwbot_config.txt"

ALT_VK = Key.alt.value.vk
TAB_VK = Key.tab.value.vk
CTRL_VK = Key.ctrl.value.vk
SHIFT_VK = Key.shift.value.vk
DEL_VK = Key.delete.value.vk
