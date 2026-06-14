from contextlib import contextmanager
from typing import final, override

from pydantic import Field
from pynput.keyboard import Controller as _PynputKeyboardController, Key, KeyCode

from bot.models.base_model import BotBaseModel, Command, KeyboardExecutor
from bot.models.timer import SleepCommand

_default_keyboard_executor: KeyboardExecutor = _PynputKeyboardController()  # pyright: ignore[reportAssignmentType]


class BaseKey(BotBaseModel):
    key: str
    vk: int | None = None
    hold: SleepCommand = Field(default_factory=SleepCommand)

    @property
    def key_code(self) -> KeyCode:
        return KeyCode.from_vk(self.vk) if self.vk else KeyCode.from_char(self.key)


@final
class ModifierKey(BaseKey):
    @override
    def __repr__(self) -> str:
        key_repr = self.key.split("_")[0]
        return key_repr.capitalize()

    @contextmanager
    def execute(self, executor: KeyboardExecutor | None = None):  # type: ignore[override]
        kb = executor or _default_keyboard_executor
        with kb.pressed(self.key_code):
            yield


@final
class Keystroke(BaseKey, Command):
    modifier: ModifierKey | None = None
    hold: SleepCommand = Field(default_factory=SleepCommand)

    @override
    def __repr__(self) -> str:
        try:
            key_repr = self.key.split("_")[1]
        except IndexError:
            key_repr = self.key
        if self.modifier:
            return f"{self.modifier!r}+{key_repr.upper()} {self.hold!r}"
        return f"{key_repr.capitalize()} {self.hold!r}"

    @override
    def execute(self, executor: KeyboardExecutor | None = None) -> None:  # type: ignore[override]
        kb = executor or _default_keyboard_executor
        if self.modifier:
            with self.modifier.execute(executor=kb):
                return self._tap(kb)
        return self._tap(kb)

    def _tap(self, executor: KeyboardExecutor) -> None:
        with executor.pressed(self.key_code):
            self.hold.execute()


@final
class DirectionalKeystroke(BaseKey, Command):
    is_directional: bool = True  # Only for pydantic validate_model

    @override
    def __repr__(self) -> str:
        return f"{self.key.capitalize()} {self.hold!r}"

    @override
    def execute(self, executor: KeyboardExecutor | None = None) -> None:  # type: ignore[override]
        kb = executor or _default_keyboard_executor
        with kb.pressed(getattr(Key, self.key.lower())):  # pyright: ignore[reportAny]
            self.hold.execute()
