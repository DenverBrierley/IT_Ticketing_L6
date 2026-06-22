from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for the IT Helpdesk.

    Subclasses AbstractUser so we retain Django's secure authentication
    (password hashing, sessions, permissions) while adding domain fields.
    Declared at project start because changing the user model later is a
    documented Django migration pain point.
    Ref: Django docs, "Customizing authentication" / "Substituting a custom User model".
    """

    class Role(models.TextChoices):
        # A fixed set of allowed roles: any value outside this set is
        # rejected during validation rather than saved to the database.
        USER = "USER", "End User"
        AGENT = "AGENT", "Support Agent"
        ADMIN = "ADMIN", "Administrator"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,  # New accounts start as ordinary end users.
    )

    # Optional team/department label, e.g. "Depot Operations".
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        # Readable label used in the admin and shell, e.g. "dbrierley (Support Agent)".
        return f"{self.username} ({self.get_role_display()})"