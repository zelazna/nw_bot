from pydantic import ValidationError
from bot.core.control import modifierKey
from bot.core.worker import WorkerSignals
from pynput import keyboard, mouse

from bot.models import Keystroke, ModifierKey, MouseClick
from bot.core.KeystrokeAdapter import directionalMapping
from bot.utils import logger

MODIFIERS = [
    keyboard.Key.shift,
    keyboard.Key.alt,
    keyboard.Key.alt_l,
    keyboard.Key.ctrl,
    keyboard.Key.ctrl_l,
    keyboard.Key.cmd,
]

IGNORED = [keyboard.Key.caps_lock, keyboard.Key.tab, keyboard.Key.esc]


class Recorder:
    signals = WorkerSignals()
    modifier: keyboard.Key | None = None

    def __init__(self) -> None:
        self.keyBoardListener: keyboard.Listener = None  # type: ignore
        self.mouseListener: mouse.Listener = None  # type: ignore

    @staticmethod
    def _get_vk_and_rep(
        key: keyboard.Key | keyboard.KeyCode,
    ) -> tuple[int | None, str | None]:
        if isinstance(key, keyboard.Key):
            vk = key.value.vk
            rep = key.value.char
        else:
            vk = key.vk
            rep = key.char
        return vk, rep

    def on_press(self, key: keyboard.Key | keyboard.KeyCode | None):
        override = None
        if not key:
            return

        if key in MODIFIERS:
            logger.debug(f"got modifier key: {key!r} ignoring it for know")
            self.modifier = key
            return

        try:
            if not self.modifier:
                logger.debug(f"Get single key: {key!r}")
                if isinstance(key, keyboard.Key):
                    vk = key.value.vk
                    rep = key.value.char
                else:
                    vk = key.vk
                    rep = key.char

                if vk in directionalMapping:
                    override = directionalMapping[vk]
                    rep = override.name

                stroke = Keystroke(key=rep, vk=vk, override=override)
                self.signals.interaction.emit(stroke)
            else:
                logger.debug(
                    f"Modifier detected along key mod: {self.modifier!r}, key: {key!r}"
                )
                modifier = ModifierKey(
                    key=self.modifier.name, vk=self.modifier.value.vk
                )
                cannonical_key = self.keyBoardListener.canonical(key)

                stroke = Keystroke(
                    key=cannonical_key.char.upper(),
                    vk=key.vk,
                    modifier=modifier,
                )
                self.signals.interaction.emit(stroke)

        except (AttributeError, ValidationError):
            logger.error(f"Unhandled key: {key!r}", exc_info=True)
            return

    def on_release(self, key: keyboard.Key | keyboard.KeyCode | None):
        if key in MODIFIERS:
            self.modifier = None

    def onClick(self, x: int, y: int, button: mouse.Button, pressed: bool):
        if pressed:
            self.signals.interaction.emit(MouseClick(kind=button, pos=(x, y)))

    def start(self):
        self.keyBoardListener = keyboard.Listener(
            on_release=self.on_release, on_press=self.on_press
        )
        self.keyBoardListener.start()
        self.mouseListener = mouse.Listener(on_click=self.onClick)
        self.mouseListener.start()

    def stop(self):
        if self.keyBoardListener and self.mouseListener:
            self.keyBoardListener.stop()
            self.mouseListener.stop()
