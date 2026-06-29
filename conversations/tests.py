from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from conversations.models import Conversation, Message


class ConversationAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="admin123",
        )

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.conversation = Conversation.objects.create(
            customer_name="John Doe",
            status="open",
        )

        Message.objects.create(
            conversation=self.conversation,
            sender="customer",
            message="Need help",
        )

    def test_conversation_list(self):
        response = self.client.get("/api/conversations/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_message_history(self):
        response = self.client.get(
            f"/api/conversations/{self.conversation.id}/messages/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_reply_api(self):
        response = self.client.post(
            f"/api/conversations/{self.conversation.id}/reply/",
            {
                "message": "Sure, I can help."
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_ai_suggestion(self):
        response = self.client.post(
            f"/api/conversations/{self.conversation.id}/suggest-reply/",
            {
                "message": "Customer wants refund"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_lock_api(self):
        response = self.client.post(
            f"/api/conversations/{self.conversation.id}/lock/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )