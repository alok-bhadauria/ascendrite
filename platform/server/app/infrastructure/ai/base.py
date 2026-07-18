from abc import ABC, abstractmethod
from typing import Any, Dict

class AIProvider(ABC):
    """
    Stable platform abstraction for Generative AI and RAG models.
    Supports swapping models or providers without changes to core curriculum indexing:
    OpenAI (SaaS) -> Gemini (SaaS) -> Anthropic (SaaS) -> Ollama (Local LLM hosting).
    """
    @abstractmethod
    async def generate_completion(self, prompt: str, model: str) -> Dict[str, Any]:
        pass
