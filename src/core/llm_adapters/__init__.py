from .llamacpp import LlamaCppLlm
from .openrouter import OpenRouterLlm

LLM_ADAPTERS = {
    "openrouter": OpenRouterLlm,
    "llama.cpp": LlamaCppLlm,
}
