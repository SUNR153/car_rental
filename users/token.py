from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime, timedelta
from django.utils.timezone import now

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"