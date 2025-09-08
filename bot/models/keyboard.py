from contextlib import contextmanager
from typing import ClassVar

from pydantic import Field
from pynput.keyboard import Controller, Key, KeyCode

from bot.models.base_model import BotBaseModel
from bot.models.timer import Timer


class BaseKey(BotBaseModel):
    key: str
    vk: int | None = None
    controller: ClassVar[Controller] = Controller()
    hold: Timer = Field(default_factory=Timer)

    @property
    def key_code(self) -> KeyCode:
        return KeyCode.from_vk(self.vk) if self.vk else KeyCode.from_char(self.key)


class ModifierKey(BaseKey):
    def __repr__(self) -> str:
        key_repr = self.key.split("_")[0]
        return key_repr.capitalize()

    @contextmanager
    def execute(self):
        with self.controller.pressed(self.key_code):
            yield


class Keystroke(BaseKey):
    modifier: ModifierKey | None = None
    hold: Timer = Field(default_factory=Timer)

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
            with self.modifier.execute():
                return self._tap()
        return self._tap()

    def _tap(self):
        with self.controller.pressed(self.key_code):
            self.hold.execute()


class DirectionalKeystroke(BaseKey):
    is_directional: bool = True  # Only for pydantic validate_model

    def __repr__(self) -> str:
        return f"{self.key.capitalize()} {self.hold!r}"

    def execute(self):
        with self.controller.pressed(getattr(Key, self.key.lower())):
            self.hold.execute()
