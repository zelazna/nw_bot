from pynput import keyboard, mouse

from bot.core.keystroke_adapter import (
    PynputKeystrokeAdapter,
)
from bot.core.worker import WorkerSignals
from bot.models import (
    Button,
    CommandsModel,
    MouseClick,
)
from bot.utils.logger import logger

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

    def __init__(self) -> None:
        self.keyBoardListener: keyboard.Listener = None  # type: ignore
        self.mouseListener: mouse.Listener = None  # type: ignore

    def onClick(self, x: int, y: int, button: mouse.Button, pressed: bool):
        if pressed:
            try:
                self.signals.interaction.emit(
                    MouseClick(kind=Button[button.name], pos=(x, y))
                )
            except KeyError:
                logger.error(f"Unknow button {button}")

    def start(self, model: CommandsModel):
        adapter = PynputKeystrokeAdapter(model)
        self.keyBoardListener = keyboard.Listener(
            on_release=adapter.on_key_release, on_press=adapter.on_key_press
        )
        self.keyBoardListener.start()
        self.mouseListener = mouse.Listener(on_click=self.onClick)
        self.mouseListener.start()

    def stop(self):
        if self.keyBoardListener and self.mouseListener:
            self.keyBoardListener.stop()
            self.mouseListener.stop()
