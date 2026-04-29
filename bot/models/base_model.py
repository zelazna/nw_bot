from pydantic import BaseModel, ConfigDict


class Command:
    def execute(self) -> None: ...


class BotBaseModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)
