from dataclasses import dataclass

from pynput import keyboard, mouse

from bot.core.keystroke_adapter import (
    PynputKeystrokeAdapter,
)
from bot.core.mouse_adapter import MouseAdapter
from bot.models import CommandListModel


@dataclass
class Recorder:
    model: CommandListModel
    keyBoardListener: keyboard.Listener | None = None
    mouseListener: mouse.Listener | None = None

    def __post_init__(self):
        self.mouse_adapter = MouseAdapter(self.model)
        self.key_adapter = PynputKeystrokeAdapter(self.model)

    def onClick(self, x: int, y: int, button: mouse.Button, pressed: bool):
        self.mouse_adapter.on_click(x, y, button, pressed)

    def start(self):
        self.keyBoardListener = keyboard.Listener(
            on_release=self.key_adapter.on_key_release,
            on_press=self.key_adapter.on_key_press,
        )
        self.keyBoardListener.start()
        self.mouseListener = mouse.Listener(on_click=self.onClick)
        self.mouseListener.start()

    def stop(self):
        if self.keyBoardListener and self.mouseListener:
            self.keyBoardListener.stop()
            self.mouseListener.stop()
