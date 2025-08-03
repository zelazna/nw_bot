from dataclasses import dataclass, field
from typing import ClassVar

from pynput.keyboard import Controller, Key, KeyCode

from bot.models.base_command import BaseCommand
from bot.models.timer import Timer


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
    hold: Timer = field(default_factory=Timer)

    def __repr__(self) -> str:
        try:
            key_repr = self.key.split("_")[1]
        except IndexError:
            key_repr = self.key
        if self.modifier:
            return f"{self.modifier!r}+{key_repr.upper()} {self.hold!r}"
        return f"{key_repr.capitalize()} {self.hold!r}"

    def execute(self):
        if self.modifier:
            self.controller.press(self.modifier.key_code)
        try:
            self.controller.press(self.key_code)
            self.hold.execute()
            self.controller.release(self.key_code)
        finally:
            if self.modifier:
                self.controller.release(self.modifier.key_code)


@dataclass
class DirectionalKeystroke(Keystroke):
    vk: int = 0

    def __repr__(self) -> str:
        return f"{self.key.capitalize()} {self.hold!r}"

    def execute(self):
        key = getattr(Key, self.key.lower())
        self.controller.press(key)
        self.hold.execute()
        self.controller.release(key)
