import random
import time
from dataclasses import dataclass

from bot.core.constants import ALT_VK, PADDING_IN_S, TAB_VK
from bot.models import Keystroke, ModifierKey, Params
from bot.utils.logger import logger

alt_tab = Keystroke(key="Tab", vk=TAB_VK, modifier=ModifierKey(key="Alt", vk=ALT_VK))


@dataclass
class Runner:
    params: Params

    def run(self):
        for _ in range(self.params.winNum):
            for command in self.params.commands:
                try:
                    logger.debug(f"Executing for {command}")
                    command.execute()
                    sleep_time = random.choice(self.params.interval_range)
                    logger.debug(f"Waiting for {sleep_time}")
                    time.sleep(sleep_time)
                    if self.params.winNum > 1:
                        alt_tab.execute()
                except TypeError:
                    logger.error(f"Command {command!r} not handled skipping")


def run(params: Params):
    time.sleep(PADDING_IN_S)  # Allow to switch window in time
    end = time.time() + params.limit * 60
    logger.info(f"Running with params:\n{params}")
    runner = Runner(params)
    while time.time() < end:
        runner.run()
