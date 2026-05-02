from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, cast, final, override

from pynput.keyboard import Key, KeyCode
from PySide6.QtCore import QElapsedTimer, Qt
from PySide6.QtGui import QKeyEvent

from bot.core.constants import ALT_VK, CTRL_VK, DEL_VK, SHIFT_VK
from bot.models import (
    CommandListModel,
    DirectionalKeystroke,
    Keystroke,
    ModifierKey,
    SleepCommand,
)
from bot.utils.logger import logger

PynputEvent = Key | KeyCode | None


@dataclass
class BaseKeyStrokeAdapter(ABC):
    model: CommandListModel
    directionalMapping: ClassVar[dict[int | None, Key]] = {
        k.value.vk: k for k in (Key.up, Key.down, Key.left, Key.right)
    }

    @abstractmethod
    def on_key_press(self, event: PynputEvent) -> None: ...

    @abstractmethod
    def on_key_release(self, event: PynputEvent) -> None: ...


@final
@dataclass
class QtKeystrokeAdapter(BaseKeyStrokeAdapter):
    upper_keys: ClassVar[tuple[str, ...]] = (
        "&", "é", '"', "'", "(", "-", "è", "_", "ç", "à", ")", "="
    )

    @override
    def on_key_press(self, event: PynputEvent) -> None: ...

    @override
    def on_key_release(self, event: PynputEvent) -> None:  # type: ignore[override]
        if not isinstance(event, QKeyEvent):
            return
        modifier = event.modifiers()
        vk: int = event.nativeVirtualKey()

        if vk in (CTRL_VK, ALT_VK, DEL_VK):
            return None

        if vk in self.directionalMapping:
            self.model.add_command(
                DirectionalKeystroke(key=self.directionalMapping[vk].name)
            )
            return

        key = Qt.Key(event.key())

        mod = None
        if modifier is not Qt.KeyboardModifier.NoModifier:
            match modifier:
                case Qt.KeyboardModifier.ControlModifier:
                    mod = ModifierKey(key="Ctrl", vk=CTRL_VK)
                case Qt.KeyboardModifier.AltModifier:
                    mod = ModifierKey(key="Alt", vk=ALT_VK)
                case Qt.KeyboardModifier.ShiftModifier:
                    mod = ModifierKey(key="Shift", vk=SHIFT_VK)
                case _:
                    pass

        if event.text() in self.upper_keys:
            keystroke = Keystroke(key=event.text())
        else:
            keystroke = Keystroke(key=key.name, vk=vk, modifier=mod)
        self.model.add_command(keystroke)


@final
@dataclass
class PynputKeystrokeAdapter(BaseKeyStrokeAdapter):
    modifier: PynputEvent = None
    current_key: PynputEvent = None
    timer: ClassVar[QElapsedTimer] = QElapsedTimer()
    modifiers: ClassVar[tuple[Key, ...]] = (
        Key.shift,
        Key.alt,
        Key.alt_l,
        Key.ctrl,
        Key.ctrl_l,
        Key.cmd,
    )

    @override
    def on_key_press(self, event: PynputEvent) -> None:
        if not event:
            return

        self.current_key = event
        self.timer.start()

        if event in self.modifiers:
            logger.debug(f"got modifier key: {event!r} storing it for know")
            self.modifier = event
            return

    @override
    def on_key_release(self, event: PynputEvent) -> None:
        if event in self.modifiers:
            self.modifier = None
            return

        try:
            timer = SleepCommand(milliseconds=self.timer.elapsed())
            if not self.modifier:
                logger.debug(f"Get single key: {event!r}")
                if isinstance(event, Key):
                    if event.value.vk in self.directionalMapping:
                        self.model.add_command(
                            DirectionalKeystroke(key=event.name, hold=timer)
                        )
                    elif event.value.vk:
                        self.model.add_command(
                            Keystroke(key=event.name, vk=event.value.vk, hold=timer)
                        )
                elif isinstance(event, KeyCode):
                    self.model.add_command(
                        Keystroke(key=cast(str, event.char), vk=event.vk, hold=timer)
                    )
            else:
                logger.debug(
                    f"Modifier detected along key mod: {self.modifier!r}, key: {event!r}"
                )
                modifier = ModifierKey(
                    key=self.modifier.name,  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]
                    vk=self.modifier.value.vk,  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]
                )

                if self.modifier in (Key.ctrl, Key.ctrl_l):
                    key = self._decode_ctrl_char(event.char)  # pyright: ignore[reportAttributeAccessIssue, reportArgumentType, reportOptionalMemberAccess, reportUnknownMemberType]
                else:
                    key = event.value.char if isinstance(event, Key) else event.char  # pyright: ignore[reportOptionalMemberAccess]

                self.model.add_command(
                    Keystroke(key=key, vk=event.vk, modifier=modifier, hold=timer)  # pyright: ignore[reportAttributeAccessIssue, reportArgumentType, reportOptionalMemberAccess, reportUnknownMemberType, reportUnknownArgumentType]
                )
            self.current_key = None

        except AttributeError:
            logger.error(f"Unhandled key: {event!r}", exc_info=True)

    def _decode_ctrl_char(self, char: str) -> str:
        val = ord(char)
        if 1 <= val <= 26:
            return chr(val + 64)  # Ex: \x01 => Ctrl + A
        return char
