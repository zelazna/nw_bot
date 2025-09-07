from pydantic import BaseModel, ConfigDict


class BotBaseModel(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)
