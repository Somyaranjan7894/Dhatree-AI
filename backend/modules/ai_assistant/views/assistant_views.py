from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from core.permissions import IsAuthenticated
from core.responses import success_response, error_response
from modules.ai_assistant.models.chat import ChatSession
from modules.ai_assistant.serializers.chat_serializers import ChatSessionSerializer
from modules.ai_assistant.services.assistant_service import AssistantService

class ChatViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSessionSerializer

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user, is_deleted=False)

    def list(self, request: Request) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data, message="Chat sessions retrieved.")

    def retrieve(self, request: Request, pk: str = None) -> Response:
        session = self.get_queryset().filter(id=pk).first()
        if not session:
            return error_response(message="Session not found.", status_code=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(session)
        return success_response(data=serializer.data, message="Chat session retrieved.")

    @extend_schema(description="Send a message to the AI assistant. (Deprecated: use /chat/ instead)")
    @action(detail=False, methods=["post"])
    def message(self, request: Request) -> Response:
        return self.chat(request)

    @extend_schema(description="Send a message to the AI assistant.")
    @action(detail=False, methods=["post"])
    def chat(self, request: Request) -> Response:
        message = request.data.get("message")
        session_id = request.data.get("session_id")
        
        if not message:
            return error_response(message="Message content is required.", status_code=status.HTTP_400_BAD_REQUEST)

        service = AssistantService()
        try:
            result = service.process_message(
                user=request.user,
                session_id=session_id,
                message=message
            )
            return success_response(data=result, message="Message processed successfully.")
        except Exception as e:
            return error_response(message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
