import json
from typing import Dict, Any, Optional
from backend.config import settings
from backend.logging import logger


class GroqClientWrapper:
    """Thread-safe OpenAI-compatible Groq API client wrapper with fallback capability."""

    def __init__(self):
        self.api_key = getattr(settings, "GROQ_API_KEY", "")
        self.default_model = getattr(settings, "GROQ_MODEL", "llama-3.3-70b-versatile")
        self._client = None
        self._initialize_client()

    def _initialize_client(self):
        if self.api_key and self.api_key.startswith("gsk_"):
            try:
                from groq import Groq
                self._client = Groq(api_key=self.api_key)
                logger.info("Successfully initialized Groq API client.")
            except Exception as e:
                logger.warning(f"Could not initialize Groq SDK: {e}. Will rely on fallback mode.")
                self._client = None
        else:
            logger.info("Groq API key not configured or standard key absent. AI agents will run in fallback deterministic mode.")

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 1024
    ) -> Optional[Dict[str, Any]]:
        """Invokes Groq API requesting structured JSON output."""
        if self._client is None:
            return None

        target_model = model or self.default_model

        try:
            response = self._client.chat.completions.create(
                model=target_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            if content:
                return json.loads(content)
        except json.JSONDecodeError as err:
            logger.error(f"Failed to parse Groq response JSON: {err}")
        except Exception as err:
            logger.error(f"Groq API call execution failed: {err}")

        return None


# Global singleton instance
groq_client = GroqClientWrapper()
