from abc import ABC, abstractmethod
from typing import Any

JsonSchema = dict[str, Any]
Json = Any

LlmAdapterExtraOutput = Any
LlmMessages = list[dict[str, Any]]


class LlmAdapter(ABC):
    @abstractmethod
    async def answer(
        self,
        messages: LlmMessages,
    ) -> tuple[str, LlmAdapterExtraOutput]: ...

    @abstractmethod
    async def answer_json(
        self,
        messages: LlmMessages,
        schema: JsonSchema,
    ) -> tuple[Json, LlmAdapterExtraOutput]: ...
