from typing import Dict, List

from modules.ai_assistant.models.chat import ChatMessage, ChatSession
from modules.ai_assistant.providers.gemini_provider import GeminiProvider


class AssistantService:
    def __init__(self):
        # Future LLM integrations will be configured here via Django settings or dynamically.
        self.provider = GeminiProvider()

    def get_or_create_session(self, user, session_id=None) -> ChatSession:
        if session_id:
            session = ChatSession.objects.filter(id=session_id, user=user).first()
            if session:
                return session

        # Snapshot context for new session (e.g. current farm count)
        context_snapshot = {
            "active_farms": (
                user.farms.filter(is_deleted=False).count()
                if hasattr(user, "farms")
                else 0
            )
        }
        return ChatSession.objects.create(
            user=user, provider_name="gemini", context_snapshot=context_snapshot
        )

    def process_message(self, user, session_id: str, message: str) -> Dict:
        """
        Processes a user message and returns the assistant's reply.
        """
        session = self.get_or_create_session(user, session_id)

        # Save user message
        ChatMessage.objects.create(
            session=session, role=ChatMessage.RoleChoices.USER, content=message
        )

        # Retrieve history
        history = list(
            session.messages.order_by("created_at").values("role", "content")
        )

        # Generate response using the provider
        response_text = self.provider.generate_response(
            user=user,
            message=message,
            context_snapshot=session.context_snapshot,
            history=history,
        )

        # Save assistant message
        assistant_msg = ChatMessage.objects.create(
            session=session,
            role=ChatMessage.RoleChoices.ASSISTANT,
            content=response_text,
        )

        return {
            "session_id": str(session.id),
            "message": response_text,
            "created_at": assistant_msg.created_at,
        }
