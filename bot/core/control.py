import random
import time
from dataclasses import dataclass

from pynput.keyboard import Controller as KeyBoardController
from pynput.mouse import Controller as MouseController

from bot.core.constants import ALT_VK, TAB_VK
from bot.models import Keystroke, ModifierKey, Params
from bot.utils import logger

mouse = MouseController()
keyboard = KeyBoardController()
alt_tab = Keystroke("Tab", TAB_VK, keyboard, ModifierKey(key="Alt", vk=ALT_VK))


@dataclass
class Runner:
    params: Params

    def run(self):
        for _ in range(self.params.winNum):
            for command in self.params.commands:
                command.execute()
                sleep_time = random.choice(self.params.interval_range)
                logger.debug("Waiting for %s", sleep_time)
                time.sleep(sleep_time)
                if self.params.winNum > 1:
                    alt_tab.execute()


def run(params: Params):
    time.sleep(5)  # Allow to switch window in time
    end = time.time() + params.limit * 60
    logger.info("run with params: %s", params)
    runner = Runner(params)
    while time.time() < end:
        runner.run()
