from .config import Config
from .llm_adapter import LlmAdapter
from .llm_adapters import LLM_ADAPTERS


class LlmStore:
    cfg: Config
    models: dict[str, LlmAdapter]

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.models = {}

    def __getitem__(self, name: str):
        if name in self.models:
            return self.models[name]

        assert name in self.cfg.llms, f"model not defined: {name}"

        cfg = self.cfg.llms[name]
        self.models[name] = LLM_ADAPTERS[cfg.type](cfg)

        return self.models[name]
