from celery import shared_task

from conversations.models import Conversation


@shared_task
def analyze_sentiment(conversation_id):
    conversation = Conversation.objects.get(id=conversation_id)

    messages = conversation.messages.all()

    text = " ".join([m.message.lower() for m in messages])

    if any(word in text for word in ["thanks", "great", "good"]):
        conversation.sentiment = "positive"

    elif any(word in text for word in ["refund", "problem", "bad", "angry"]):
        conversation.sentiment = "negative"

    else:
        conversation.sentiment = "neutral"

    conversation.save()

    return conversation.sentiment