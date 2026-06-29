from django.shortcuts import get_object_or_404
from analytics.tasks import analyze_sentiment
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from analytics.tasks import analyze_sentiment

from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ai_engine.services import AIReplyService
from locks.services import ConversationLockService

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    ReplySerializer,
)


class ConversationListAPIView(generics.ListAPIView):
    queryset = Conversation.objects.all().order_by("-created_at")
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]

    filterset_fields = ["status"]
    search_fields = ["customer_name"]


class ConversationMessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            conversation_id=self.kwargs["id"]
        ).order_by("created_at")


class ReplyAPIView(generics.GenericAPIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        conversation = get_object_or_404(Conversation, id=id)

        # Check conversation lock
        owner = ConversationLockService.owner(id)

        if owner and owner != request.user.id:
            return Response(
                {
                    "detail": "Conversation is locked by another agent."
                },
                status=status.HTTP_423_LOCKED,
            )

        # Acquire lock
        ConversationLockService.acquire(
            id,
            request.user.id,
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save agent reply
        message = Message.objects.create(
            conversation=conversation,
            sender="agent",
            message=serializer.validated_data["message"],
        )

        # Trigger background sentiment analysis
        try:
            if settings.CELERY_TASK_ALWAYS_EAGER:
                analyze_sentiment(conversation.id)
            else:
                analyze_sentiment.delay(conversation.id)
        except Exception:
            # Fallback for development if Redis/Celery is unavailable
            analyze_sentiment(conversation.id)

        # Release lock
        ConversationLockService.release(
            id,
            request.user.id,
        )

        return Response(
            {
                "success": True,
                "message_id": message.id,
                "message": "Reply sent successfully.",
            },
            status=status.HTTP_201_CREATED,
        )

class SuggestReplyAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        message = request.data.get("message", "")

        suggestion = AIReplyService.suggest(message)

        return Response(
            {
                "suggestion": suggestion,
            }
        )


class AcquireLockAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        locked = ConversationLockService.acquire(
            id,
            request.user.id,
        )

        return Response(
            {
                "locked": locked,
                "owner": ConversationLockService.owner(id),
            }
        )


class ReleaseLockAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        released = ConversationLockService.release(
            id,
            request.user.id,
        )

        return Response(
            {
                "released": released,
            }
        )
class LockStatusAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        owner = ConversationLockService.owner(id)

        return Response(
            {
                "conversation_id": id,
                "locked": owner is not None,
                "owner": owner,
            }
        )
        