from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field

from .llm_adapters.llamacpp import LlamaCppLlm
from .llm_adapters.openrouter import OpenRouterLlm

# TODO: generate this automatically


class OpenRouterConfig_(OpenRouterLlm.Config):
    type: Literal["openrouter"]


class LlamaCppConfig_(LlamaCppLlm.Config):
    type: Literal["llama.cpp"]


LlmConfig = Annotated[LlamaCppConfig_ | OpenRouterConfig_, Field(discriminator="type")]


class Config(BaseModel):
    llms: dict[str, LlmConfig]
    summarizer: str
    extractor: str
