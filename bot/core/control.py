import time
from typing import Callable

from bot.core.constants import ALT_VK, PADDING_IN_S, TAB_VK
from bot.models import Keystroke, ModifierKey, Params, SleepRandomCommand
from bot.utils.logger import logger


alt_tab = Keystroke(key="Tab", vk=TAB_VK, modifier=ModifierKey(key="Alt", vk=ALT_VK))


def run(params: Params, on_command: Callable[[int], None] | None = None) -> None:
    sleep = SleepRandomCommand(interval_range=params.interval_range)
    logger.info(f"Running with params:\n{params}")
    time.sleep(PADDING_IN_S)
    end = time.time() + params.limit * 60
    while time.time() < end:
        for _ in range(params.winNum):
            for i, cmd in enumerate(params.commands):
                if on_command and not isinstance(cmd, SleepRandomCommand):
                    on_command(i)
                try:
                    logger.debug(f"Executing {cmd}")
                    cmd.execute()
                except TypeError:
                    logger.error(f"Command {cmd!r} not handled skipping")
                sleep.execute()
                if params.winNum > 1:
                    alt_tab.execute()
