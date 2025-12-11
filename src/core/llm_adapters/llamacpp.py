import json

from pydantic import BaseModel, Field
from openai import AsyncOpenAI

from ..llm_adapter import LlmAdapter


class LlamaCppLlm(LlmAdapter):
    class Config(BaseModel):
        model: str
        base_url: str | None = Field(default=None)
        api_key: str | None = Field(default=None)

    model: str
    client: AsyncOpenAI

    def __init__(self, cfg: Config):
        self.model = cfg.model

        base_url = cfg.base_url or "http://127.0.0.1:8080"
        api_key = cfg.api_key or ""

        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    async def answer(self, messages):
        resp = await self.client.chat.completions.create(
            messages=messages,
            model=self.model,
        )
        return resp.choices[0].message.content

    async def answer_json(self, messages, schema):
        resp = await self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            response_format={
                "type": "json_object",
                "schema": schema,
            },
        )

        out_str = resp.choices[0].message.content
        out_json = json.loads(out_str)

        return out_json
