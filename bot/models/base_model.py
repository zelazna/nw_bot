from typing import ClassVar, Protocol

from pydantic import BaseModel, ConfigDict


class KeyboardExecutor(Protocol):
    def pressed(self, key): ...


class MouseExecutor(Protocol):
    def click(self, button) -> None: ...


class Command:
    is_reportable: ClassVar[bool] = True

    def execute(self) -> None: ...


class BotBaseModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)
