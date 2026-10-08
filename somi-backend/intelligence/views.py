import json

from django.http import StreamingHttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .assistant import AIAssistantService
from .services import IntelligenceEngine


class IntelligenceOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        engine = IntelligenceEngine(user=request.user)

        return Response(
            engine.full_summary()
        )


class AIAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get("message", "")
        stream = request.data.get("stream", False)

        if not isinstance(message, str):
            return Response(
                {
                    "detail": "The message must be a text value."
                },
                status=400,
            )

        message = message.strip()

        if not message:
            return Response(
                {
                    "detail": "Please provide a message."
                },
                status=400,
            )

        # Normalize stream value because JSON/form requests
        # may send it as a boolean or string.
        if isinstance(stream, str):
            stream = stream.lower() in (
                "true",
                "1",
                "yes",
            )

        if stream:
            try:
                assistant = AIAssistantService(
                    user=request.user
                )

                response = StreamingHttpResponse(
                    self._stream_response(
                        assistant,
                        message,
                    ),
                    content_type="application/x-ndjson",
                )

                response["Cache-Control"] = "no-cache"
                response["X-Accel-Buffering"] = "no"

                return response

            except RuntimeError as error:
                return Response(
                    {
                        "detail": str(error),
                        "source": "somi_ai",
                    },
                    status=503,
                )

        try:
            assistant = AIAssistantService(
                user=request.user
            )

            result = assistant.answer(message)

        except RuntimeError as error:
            return Response(
                {
                    "detail": str(error),
                    "source": "somi_ai",
                },
                status=503,
            )

        return Response(
            {
                "message": message,
                "answer": result["answer"],
                "source": result["source"],
                "provider": result.get("provider"),
                "model": result.get("model"),
            }
        )

    def _stream_response(self, assistant, message):
        try:
            for chunk in assistant.stream_answer(message):
                yield (
                    json.dumps(
                        chunk,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

        except Exception as error:
            yield (
                json.dumps(
                    {
                        "type": "error",
                        "detail": str(error),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )