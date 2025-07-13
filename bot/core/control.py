import ctypes
import time
from typing import TypedDict
import logging

SendInput = ctypes.windll.user32.SendInput
logger = logging.getLogger(__name__)

# DirectX scan codes https://gist.github.com/tracend/912308
KEYMAP = {
    "A": 0x1E,
    "Z": 0x2C,
    "Q": 0x10,
    "W": 0x11,
    "E": 0x12,
    "R": 0x13,
    "T": 0x14,
    "Y": 0x15,
    "U": 0x16,
    "I": 0x17,
    "O": 0x18,
    "P": 0x19,
    "ALT": 0x38,
    "TAB": 0x0F,
    "SPACE": 0x39,
    "4": 0x05,
    "5": 0x06,
    "6": 0x07,
    "7": 0x08,
}


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
    logging.debug("Window change")
    press_key(KEYMAP["ALT"])
    press_key(KEYMAP["TAB"])
    time.sleep(0.5)
    release_key(KEYMAP["TAB"])
    release_key(KEYMAP["ALT"])


def keystroke(key: str) -> None:
    key_code = KEYMAP[key.upper()]
    logging.debug("Keystroke %s", key)
    press_key(key_code)
    time.sleep(0.5)
    release_key(key_code)


class ParamsDict(TypedDict):
    limit: int
    keys: list[str]
    win_num: int
    interval: int


def run(params: ParamsDict):
    end = time.time() + params["limit"] * 60
    logger.debug("run with params: %s", params)
    while time.time() < end:
        for _ in range(params["win_num"]):
            for key in params["keys"]:
                keystroke(key)
                time.sleep(params["interval"])
            if params["win_num"] > 1:
                change_window()
