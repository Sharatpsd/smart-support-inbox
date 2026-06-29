from django.urls import path 

from .views import (
    ConversationListAPIView,
    ConversationMessageListAPIView,
)
from .views import (
    ConversationListAPIView,
    ConversationMessageListAPIView,
    ReplyAPIView,
    SuggestReplyAPIView,
    AcquireLockAPIView,
    ReleaseLockAPIView,
    LockStatusAPIView,
)
urlpatterns = [
    path(
        "conversations/",
        ConversationListAPIView.as_view(),
        name="conversation-list",
    ),
    path(
        "conversations/<int:id>/messages/",
        ConversationMessageListAPIView.as_view(),
        name="conversation-messages",
    ),
    path(
    "conversations/<int:id>/reply/",
    ReplyAPIView.as_view(),
    name="conversation-reply",
),

path(
    "conversations/<int:id>/suggest-reply/",
    SuggestReplyAPIView.as_view(),
    name="suggest-reply",
),
path(
    "conversations/<int:id>/lock/",
    AcquireLockAPIView.as_view(),
),
path(
    "conversations/<int:id>/unlock/",
    ReleaseLockAPIView.as_view(),
),
path(
    "conversations/<int:id>/lock-status/",
    LockStatusAPIView.as_view(),
    name="lock-status",
),
]