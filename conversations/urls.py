from django.urls import path
from .views import ConversationListAPIView

urlpatterns = [
    path(
        "conversations/",
        ConversationListAPIView.as_view(),
        name="conversation-list",
    ),
]