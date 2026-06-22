from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #Custom user model for the IT Helpdesk.



    class Role(models.TextChoices):
        USER = "USER", "End User"
        AGENT = "AGENT", "Support Agent"
        ADMIN = "ADMIN", "Administrator"

    # Governs what each user can see and do throughout the app.
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )

    # Optional team/department label, e.g. "Depot Operations".
    department = models.CharField(max_length=100, blank=True)


    # These keep permission checks readable ("if user.is_support_staff")
    # instead of scattering role-string comparisons across the codebase.

    @property
    def is_agent(self):
        """True if this user is a support agent."""
        return self.role == self.Role.AGENT

    @property
    def is_administrator(self):
        """True if this user is an administrator (distinct from Django's is_staff)."""
        return self.role == self.Role.ADMIN

    @property
    def is_support_staff(self):
        """Agents and admins can both work on any ticket; end users cannot."""
        return self.role in {self.Role.AGENT, self.Role.ADMIN}

    def __str__(self):
        # Readable label used in the admin and shell, e.g. "dbrierley (Support Agent)".
        return f"{self.username} ({self.get_role_display()})"