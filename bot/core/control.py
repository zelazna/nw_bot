import ctypes
import logging
import random
import time
from contextlib import contextmanager
from typing import Generator, TypedDict

from bot.core.keystroke_adapter import ALT_TAB, Keystroke
from bot.utils import logger

SendInput = ctypes.windll.user32.SendInput


# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort),
    ]


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]


# Actual Functions
def press_key(hex_key_code: int):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(hex_key_code: int):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def change_window():
    keystroke(ALT_TAB)


@contextmanager
def modifier_key(stroke: Keystroke) -> Generator[Keystroke, None, None]:
    if stroke.modifier:
        press_key(stroke.modifier.scan_code)
    try:
        yield stroke
    finally:
        if stroke.modifier:
            release_key(stroke.modifier.scan_code)


def keystroke(stroke: Keystroke, hold_sec: float = 0.5) -> None:
    logging.debug("Keystroke %s", stroke)

    with modifier_key(stroke) as stroke:
        press_key(stroke.scan_code)
        time.sleep(hold_sec)
        release_key(stroke.scan_code)


class ParamsDict(TypedDict):
    limit: int
    keys: list[Keystroke]
    win_num: int
    interval: list[int]


def run(params: ParamsDict):
    time.sleep(5)  # Allow to switch window in time
    end = time.time() + params["limit"] * 60
    logger.debug("run with params: %s", params)
    while time.time() < end:
        for _ in range(params["win_num"]):
            for stroke in params["keys"]:
                keystroke(stroke)
                sleep_time = random.choice(params["interval"])
                logger.debug("Waiting for %s", sleep_time)
                time.sleep(sleep_time)
            if params["win_num"] > 1:
                change_window()
