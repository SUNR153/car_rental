# users/token.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime, timedelta
from django.utils.timezone import now

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

    def check_token(self, user, token):
        if not super().check_token(user, token):
            return False

        # Проверяем, не истёк ли срок токена (30 минут)
        try:
            ts_built_in = int(token.split("-")[1])
            created_time = datetime.fromtimestamp(ts_built_in)
            if now() - created_time > timedelta(minutes=30):
                return False
        except Exception:
            return False

        return True
