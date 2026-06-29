from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "status",
        "sentiment",
        "created_at",
    )
    search_fields = ("customer_name",)
    list_filter = ("status", "sentiment")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "sender",
        "created_at",
    )