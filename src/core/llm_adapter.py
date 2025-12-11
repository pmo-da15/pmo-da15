from abc import ABC, abstractmethod
from typing import Any

from .misc import JsonSchema

LlmMessages = list[dict[str, Any]]


class LlmAdapter(ABC):
    @abstractmethod
    async def answer(
        self,
        messages: LlmMessages,
    ) -> str: ...

    @abstractmethod
    async def answer_json(
        self,
        messages: LlmMessages,
        schema: JsonSchema,
    ) -> Any: ...
