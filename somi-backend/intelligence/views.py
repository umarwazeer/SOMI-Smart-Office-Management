from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .assistant import AIAssistantService
from .services import IntelligenceEngine


class IntelligenceOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        engine = IntelligenceEngine(user=request.user)
        return Response(engine.full_summary())


class AIAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get("message", "")

        if not isinstance(message, str):
            return Response(
                {
                    "detail": "The message must be a text value."
                },
                status=400,
            )

        assistant = AIAssistantService(user=request.user)
        result = assistant.answer(message)

        return Response(
            {
                "message": message,
                "answer": result["answer"],
                "source": result["source"],
            }
        )