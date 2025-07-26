import logging
import random
import time
from contextlib import contextmanager
from typing import Generator

from pynput.keyboard import Controller

from bot.core.keystroke_adapter import ALT_TAB, Keystroke
from bot.models import Params
from bot.utils import logger

keyboard = Controller()


def change_window():
    # TODO: Use win32gui.SetForegroundWindow instead of ALT_TAB
    # https://github.com/learncodebygaming/multiple-minimized-windows
    keystroke(ALT_TAB)


@contextmanager
def modifier_key(stroke: Keystroke) -> Generator[Keystroke, None, None]:
    if stroke.modifier:
        keyboard.press(stroke.modifier.key_code)
    try:
        yield stroke
    finally:
        if stroke.modifier:
            keyboard.release(stroke.modifier.key_code)


def keystroke(stroke: Keystroke, hold_sec: float = 0.2) -> None:
    logging.debug("Keystroke %s", stroke)
    with modifier_key(stroke) as stroke:
        keyboard.press(stroke.key_code)
        time.sleep(hold_sec)
        keyboard.release(stroke.key_code)


def run(params: Params):
    time.sleep(5)  # Allow to switch window in time
    end = time.time() + params.limit * 60
    logger.debug("run with params: %s", params)
    while time.time() < end:
        for _ in range(params.win_num):
            for stroke in params.keys:
                keystroke(stroke)
                sleep_time = random.choice(params.interval_range)
                logger.debug("Waiting for %s", sleep_time)
                time.sleep(sleep_time)
                if params.win_num > 1:
                    change_window()
