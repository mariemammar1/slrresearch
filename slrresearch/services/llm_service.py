import json
import os
import urllib.request
import urllib.error

from dotenv import load_dotenv

load_dotenv()


class LLMService:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama")
        self.model = os.getenv("LLM_MODEL", "")
        self.base_url = os.getenv(
            "LLM_BASE_URL", "http://localhost:11434"
        ).rstrip("/")

        if self.provider != "ollama":
            raise ValueError(
                f"Unsupported LLM provider: {self.provider}"
            )

        if not self.model:
            raise ValueError("LLM_MODEL is not configured in .env")

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format=None,
    ):
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
        }

        if response_format is not None:
            payload["format"] = response_format

        request = urllib.request.Request(
            url=f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                result = json.loads(response.read().decode("utf-8"))

            content = result["message"]["content"]

            if response_format is not None:
                return json.loads(content)

            return content

        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"Failed to communicate with Ollama: {exc}"
            ) from exc

        except (KeyError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                "Invalid response received from Ollama."
            ) from exc