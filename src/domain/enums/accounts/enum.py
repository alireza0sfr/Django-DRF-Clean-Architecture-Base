from django.db import models


class BanReasons(models.TextChoices):
    ABUSIVE = 'Abusive'
    RACISM = 'Racism'
    SPAM = 'Spam'
    SUSPICIOUS_ACTIVITY = 'Suspicious Activity'
    OTHER = 'OTHER'
