import re


class AIReplyService:

    REPLIES = {
        r"refund": "We are sorry for the inconvenience. Your refund request has been received.",
        r"order": "Thank you for contacting us. We are checking your order.",
        r"payment": "Please verify your payment information and try again.",
        r"delay": "We sincerely apologize for the delay. Our team is looking into it.",
    }

    @classmethod
    def suggest(cls, message):
        text = message.lower()

        for pattern, reply in cls.REPLIES.items():
            if re.search(pattern, text):
                return reply

        return (
            "Thank you for contacting support. "
            "Our support team will get back to you shortly."
        )