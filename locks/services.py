from django.core.cache import cache

LOCK_TIMEOUT = 300  # 5 minutes


class ConversationLockService:

    @staticmethod
    def lock_key(conversation_id):
        return f"conversation_lock:{conversation_id}"

    @classmethod
    def acquire(cls, conversation_id, user_id):
        key = cls.lock_key(conversation_id)

        if cache.get(key):
            return False

        cache.set(key, user_id, timeout=LOCK_TIMEOUT)
        return True

    @classmethod
    def release(cls, conversation_id, user_id):
        key = cls.lock_key(conversation_id)

        owner = cache.get(key)

        if owner == user_id:
            cache.delete(key)
            return True

        return False

    @classmethod
    def owner(cls, conversation_id):
        return cache.get(cls.lock_key(conversation_id))