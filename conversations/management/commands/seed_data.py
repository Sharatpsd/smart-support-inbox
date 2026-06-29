from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from conversations.models import Conversation, Message


class Command(BaseCommand):
    help = "Seed initial project data"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@test.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:
            admin.set_password("admin123")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Admin user created."))
        else:
            self.stdout.write(self.style.WARNING("Admin already exists."))

        if Conversation.objects.exists():
            self.stdout.write(
                self.style.WARNING("Sample conversations already exist.")
            )
            return

        # Conversation 1
        conversation1 = Conversation.objects.create(
            customer_name="John Doe",
            status="open",
            sentiment="neutral",
        )

        Message.objects.create(
            conversation=conversation1,
            sender="customer",
            message="Need help with my order.",
        )

        Message.objects.create(
            conversation=conversation1,
            sender="agent",
            message="Sure, I can help you.",
        )

        # Conversation 2
        conversation2 = Conversation.objects.create(
            customer_name="Alice Smith",
            status="pending",
            sentiment="positive",
        )

        Message.objects.create(
            conversation=conversation2,
            sender="customer",
            message="I want a refund.",
        )

        Message.objects.create(
            conversation=conversation2,
            sender="agent",
            message="We are reviewing your request.",
        )

        self.stdout.write(
            self.style.SUCCESS("Sample data created successfully.")
        )