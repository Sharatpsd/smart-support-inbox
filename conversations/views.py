from django.conf import settings
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from analytics.tasks import analyze_sentiment
from ai_engine.services import AIReplyService
from locks.services import ConversationLockService

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    ReplySerializer,
)


@extend_schema(
    tags=["Conversations"],
    summary="List conversations",
    description="Returns paginated conversations with search and status filtering.",
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


@extend_schema(
    tags=["Messages"],
    summary="Conversation message history",
    description="Returns all messages for a conversation ordered by time.",
)
class ConversationMessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            conversation_id=self.kwargs["id"]
        ).order_by("created_at")


@extend_schema(
    tags=["Replies"],
    summary="Reply to a conversation",
    description="Allows an authenticated support agent to send a reply.",
)
class ReplyAPIView(generics.GenericAPIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        conversation = get_object_or_404(Conversation, id=id)

        owner = ConversationLockService.owner(id)

        if owner and owner != request.user.id:
            return Response(
                {
                    "detail": "Conversation is locked by another agent."
                },
                status=status.HTTP_423_LOCKED,
            )

        ConversationLockService.acquire(
            id,
            request.user.id,
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = Message.objects.create(
            conversation=conversation,
            sender="agent",
            message=serializer.validated_data["message"],
        )

        try:
            if settings.CELERY_TASK_ALWAYS_EAGER:
                analyze_sentiment(conversation.id)
            else:
                analyze_sentiment.delay(conversation.id)
        except Exception:
            analyze_sentiment(conversation.id)

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


@extend_schema(
    tags=["AI"],
    summary="Generate AI reply suggestion",
    description="Returns a rule-based AI suggestion based on the customer's message.",
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


@extend_schema(
    tags=["Locks"],
    summary="Acquire conversation lock",
    description="Locks a conversation for the current support agent.",
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


@extend_schema(
    tags=["Locks"],
    summary="Release conversation lock",
    description="Releases the conversation lock owned by the current support agent.",
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


@extend_schema(
    tags=["Locks"],
    summary="Get conversation lock status",
    description="Returns the current lock status and lock owner.",
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