import logging
import random
import time
from contextlib import contextmanager
from typing import Generator

from pynput.keyboard import Controller as KeyBoardController
from pynput.mouse import Controller as MouseController

from bot.core.KeystrokeAdapter import ALT_TAB
from bot.models import Keystroke, MouseClick, Params
from bot.utils import logger

mouse = MouseController()
keyboard = KeyBoardController()


def changeWindow():
    # TODO: Use win32gui.SetForegroundWindow instead of ALT_TAB
    # https://github.com/learncodebygaming/multiple-minimized-windows
    keystroke(ALT_TAB)


@contextmanager
def modifierKey(stroke: Keystroke) -> Generator[Keystroke, None, None]:
    if stroke.modifier:
        keyboard.press(stroke.modifier.key_code)
    try:
        yield stroke
    finally:
        if stroke.modifier:
            keyboard.release(stroke.modifier.key_code)


def keystroke(stroke: Keystroke, hold_sec: float = 0.2) -> None:
    logging.debug("Keystroke %s", stroke)
    with modifierKey(stroke) as stroke:
        keyboard.press(stroke.key_code)
        time.sleep(hold_sec)
        keyboard.release(stroke.key_code)


def mouseClick(click: "MouseClick", hold_sec: float = 0.2):
    mouse.press(click.kind)
    time.sleep(hold_sec)
    mouse.release(click.kind)


def run(params: Params):
    time.sleep(5)  # Allow to switch window in time
    end = time.time() + params.limit * 60
    logger.info("run with params: %s", params)
    while time.time() < end:
        for _ in range(params.winNum):
            for command in params.commands:

                if isinstance(command, Keystroke):
                    keystroke(command)
                else:
                    mouseClick(command)

                sleep_time = random.choice(params.interval_range)
                logger.debug("Waiting for %s", sleep_time)
                time.sleep(sleep_time)
                if params.winNum > 1:
                    changeWindow()
