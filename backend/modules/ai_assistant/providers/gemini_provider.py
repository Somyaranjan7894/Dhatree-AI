import json
import logging
import os
from typing import Dict, List

from google import genai
from google.genai import types
from google.genai.errors import APIError

from modules.ai_assistant.prompts import SYSTEM_PROMPT

from .base import BaseProvider

logger = logging.getLogger(__name__)


class GeminiProvider(BaseProvider):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = os.getenv("GEMINI_MODEL", model_name)
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            logger.error("GEMINI_API_KEY is not set in the environment variables.")

        # Initialize the client only if the key is available
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def _format_history(self, history: List[Dict]) -> List[types.Content]:
        formatted = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            formatted.append(
                types.Content(
                    role=role, parts=[types.Part.from_text(text=msg["content"])]
                )
            )
        return formatted

    def generate_response(
        self, user, message: str, context_snapshot: Dict, history: List[Dict]
    ) -> str:
        if not self.client:
            return "Configuration Error: The AI Assistant API key is missing. Please contact the administrator."

        try:
            # Prepare contextual prompt
            context_str = json.dumps(context_snapshot, indent=2, default=str)
            full_prompt = (
                f"{SYSTEM_PROMPT}\n\n"
                f"### CURRENT USER CONTEXT:\n{context_str}\n\n"
                f"User Message:\n{message}"
            )

            # Format previous history
            formatted_history = self._format_history(history)

            # Call Gemini
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=formatted_history
                + [
                    types.Content(
                        role="user", parts=[types.Part.from_text(text=full_prompt)]
                    )
                ],
            )

            if not response or not response.text:
                logger.error("Received an empty response from Gemini API.")
                return "I'm sorry, I couldn't generate a response at this time. Please try again later."

            return response.text

        except APIError as e:
            # Handle standard GenAI SDK errors gracefully without exposing keys
            logger.error(f"Gemini API Error: {e.message}")
            if getattr(e, "code", 0) == 429:
                return "The AI Assistant is currently experiencing high traffic. Please try again in a few moments."
            elif getattr(e, "code", 0) in [401, 403]:
                return "Configuration Error: Unauthorized. Please check the AI Assistant configuration."
            return "I encountered an error communicating with the intelligence service. Please try again later."
        except Exception as e:
            logger.error(f"Unexpected error in GeminiProvider: {str(e)}")
            return "An unexpected error occurred while processing your request. Please try again later."
