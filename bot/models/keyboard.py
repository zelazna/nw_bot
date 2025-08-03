import time
from dataclasses import dataclass
from typing import ClassVar

from pynput.keyboard import Controller, Key, KeyCode

from bot.models.base_command import BaseCommand


@dataclass
class BaseKey:
    key: str
    vk: int

    @property
    def key_code(self) -> KeyCode | Key:
        return KeyCode.from_vk(self.vk)


class ModifierKey(BaseKey):
    def __repr__(self) -> str:
        key_repr = self.key.split("_")[0]
        return key_repr.capitalize()


@dataclass
class Keystroke(BaseKey, BaseCommand):
    modifier: ModifierKey | None = None
    controller: ClassVar[Controller] = Controller()
    hold_sec: float = 0.2

    def __repr__(self) -> str:
        try:
            key_repr = self.key.split("_")[1]
        except IndexError:
            key_repr = self.key
        if self.modifier:
            return f"{self.modifier!r}+{key_repr.upper()}"
        return key_repr.capitalize()

    def execute(self):
        if self.modifier:
            self.controller.press(self.modifier.key_code)
        try:
            self.controller.press(self.key_code)
            time.sleep(self.hold_sec)
            self.controller.release(self.key_code)
        finally:
            if self.modifier:
                self.controller.release(self.modifier.key_code)


@dataclass
class DirectionalKeystroke(Keystroke):
    vk: int = 0

    def __repr__(self) -> str:
        return self.key.capitalize()

    def execute(self):
        key = getattr(Key, self.key)
        self.controller.press(key)
        time.sleep(self.hold_sec)
        self.controller.release(key)
