import json

from pydantic import BaseModel
import aiohttp

from ..llm_adapter import LlmAdapter

API_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterLlm(LlmAdapter):
    class Config(BaseModel):
        model: str
        api_key: str

    model: str
    api_key: str

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    async def _request(self, json_body):
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            json_body_ = {"model": self.model, **json_body}

            async with session.post(API_URL, headers=headers, json=json_body_) as resp:
                return resp

    async def answer(self, messages):
        resp = await self._request({"messages": messages})
        resp_json = await resp.json()
        return resp_json["choices"][0]["message"]["content"]

    async def answer_json(self, messages, schema):
        resp = await self._request(
            {
                "messages": messages,
                "response_format": {
                    "type": "json_schema",
                    "json_schema": schema,
                },
            }
        )

        resp_json = await resp.json()
        out_str = resp_json["choices"][0]["message"]["content"]
        out_json = json.loads(out_str)

        return out_json
