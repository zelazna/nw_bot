import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# directx scan codes https://gist.github.com/tracend/912308
E_KEY = 0x12
R_KEY = 0x13
Q_KEY = 0x10
ALT_KEY = 0x38
TAB_KEY = 0x0F
DIK_SPACE = 0x39
DIK_4 = 0x05
DIK_5 = 0x06
DIK_6 = 0x07
DIK_7 = 0x08

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


# Actuals Functions


def press_key(hex_key_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(hex_key_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def change_window():
    press_key(ALT_KEY)
    press_key(TAB_KEY)
    time.sleep(1)
    release_key(TAB_KEY)
    release_key(ALT_KEY)


def launch_encounter(key):
    press_key(key)
    time.sleep(1)
    release_key(key)


def share_hospitality():
    def inner():
        for i in [DIK_4, DIK_5, DIK_6]:
            launch_encounter(i)
            time.sleep(1)
            launch_encounter(DIK_SPACE)
            time.sleep(2)
    inner()
    change_window()
    inner()
    change_window()


def farm_stuff():
    launch_encounter(E_KEY)
    change_window()
    time.sleep(1)
    launch_encounter(E_KEY)
    time.sleep(5)


while True:
    share_hospitality()
