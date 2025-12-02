import json
from openai import AsyncOpenAI

from src.llms.adapter import LlmAdapter


class LlamaCppLlm(LlmAdapter):
    model: str

    def __init__(self, model: str):
        self.model = model

        self.client = AsyncOpenAI(
            base_url="http://127.0.0.1:8080",
            api_key="",
        )

    async def answer(self, messages):
        resp = await self.client.chat.completions.create(
            messages=messages,
            model=self.model,
        )
        return resp.choices[0].message.content, resp

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

        return out_json, resp
