# DirectX scan codes https://gist.github.com/tracend/912308
KEYMAP = {
    "ESPACE": 0x39,
    "A": 0x1E,
    "Z": 0x2C,
    "E": 0x12,
    "W": 0x11,
    "Q": 0x10,
    "R": 0x13,
    "T": 0x14,
    "Y": 0x15,
    "U": 0x16,
    "I": 0x17,
    "O": 0x18,
    "P": 0x19,
    "ALT": 0x38,
    "TAB": 0x0F,
    "ECHAP": 0x01,
    "CTRL": 0x1D,
    "3": 0x04,
    "4": 0x05,
    "5": 0x06,
    "6": 0x07,
    "7": 0x08,
}

INVERTED_KEYMAP = {v: k for k, v in KEYMAP.items()}

ALT = KEYMAP["ALT"]
CTRL = KEYMAP["CTRL"]