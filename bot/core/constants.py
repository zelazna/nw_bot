from typing import cast

from pynput.keyboard import Key

ALT_VK = cast(int, Key.alt.value.vk)
TAB_VK = cast(int, Key.tab.value.vk)
CTRL_VK = cast(int, Key.ctrl.value.vk)
