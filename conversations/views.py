from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import filters, generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ai_engine.services import AIReplyService

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

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = Message.objects.create(
            conversation=conversation,
            sender="agent",
            message=serializer.validated_data["message"],
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
                "suggestion": suggestion
            }
        )