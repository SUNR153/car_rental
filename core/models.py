from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # автоматом при создании
    updated_at = models.DateTimeField(auto_now=True)      # автоматом при обновлении

    class Meta:
        abstract = True  # не создаёт таблицу, просто наследуется
