from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "USER", "End User"
        AGENT = "AGENT", "Support Agent"
        ADMIN = "ADMIN", "Administrator"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
