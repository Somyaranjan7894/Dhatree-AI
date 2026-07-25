from abc import ABC, abstractmethod
from typing import Dict, List


class BaseProvider(ABC):
    """
    Abstract Base Class for AI Assistant Providers.
    Allows swapping between a rule-based engine and future LLM providers (e.g. OpenAI, Vertex AI).
    """

    @abstractmethod
    def generate_response(
        self, user, message: str, context_snapshot: Dict, history: List[Dict]
    ) -> str:
        """
        Generate a response based on the user's message, current context snapshot, and chat history.

        Args:
            user: The User instance making the request.
            message: The current user message.
            context_snapshot: Contextual data (e.g. recent predictions, farms) attached to the session.
            history: List of previous messages in the format [{'role': 'user'/'assistant', 'content': '...'}]

        Returns:
            str: The assistant's response.
        """
        pass
