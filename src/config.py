from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field


class OpenRouterConfig(BaseModel):
    type: Literal["openrouter"]
    model: str
    api_key: str


class LlamaCppConfig(BaseModel):
    type: Literal["llamacpp"]
    model: str


LlmConfig = Annotated[LlamaCppConfig | OpenRouterConfig, Field(discriminator="type")]


class Config(BaseModel):
    llms: dict[str, LlmConfig]
