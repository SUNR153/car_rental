from .models import User
from django.utils import timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp):
        login_time = timezone.datetime.timestamp(user.date_joined)
        return (
            str(user.pk) +
            str(timestamp) +
            str(user.is_active) +
            str(login_time)
        )
