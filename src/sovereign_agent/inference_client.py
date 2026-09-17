import os
import httpx


INFERENCE_SERVICE_URL = os.getenv(
    "INFERENCE_SERVICE_URL",
    "http://localhost:8001/generate"
)

DEFAULT_MODEL = os.getenv(
    "SOVEREIGN_MODEL",
    "qwen3:4b-instruct-2507-q4_K_M"
)


class LocalLLMResponse:
    def __init__(self, content: str):
        self.content = content


class LocalLLM:

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL,
        temperature: float = 0.2,
        max_tokens: int = 1024,
        top_p: float = 0.9
    ):
        self.model_id = model_id
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p

    def invoke(self, prompt: str) -> LocalLLMResponse:

        payload = {
            "model_id": self.model_id,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "config": {
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p
            }
        }

        try:
            response = httpx.post(
                INFERENCE_SERVICE_URL,
                json=payload,
                timeout=300
            )

            response.raise_for_status()

            data = response.json()

            return LocalLLMResponse(
                data["response"]
            )

        except httpx.HTTPError as e:
            raise RuntimeError(
                f"Inference service error: {e}"
            )

        except KeyError:
            raise RuntimeError(
                "Inference service returned an invalid response."
            )