from django.conf import settings
from django.db import models


class Category(models.Model): #Ticket Categories

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"  # Avoids the use of "Categorys" in the admin panel.
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ticket(models.Model): #Tickets

    # Fixed sets of allowed values. Using TextChoices means invalid values
    # are rejected on validation rather than written to the database.
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        URGENT = "URGENT", "Urgent"

    title = models.CharField(max_length=120)
    description = models.TextField()

    # Foreign Key: each ticket belongs to one category; PROTECT stops a category
    # being deleted while tickets still reference it.
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="tickets",
    )

    # Foreign Key: the user who raised the ticket. references the user model via
    # settings.AUTH_USER_MODEL  so this keeps working
    # with custom user. CASCADE - if the user is deleted, their tickets go too.
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tickets",
    )

    # Foriegn Key: the agent handling it. Nullable because new tickets are unassigned.
    # SET_NULL: if that agent's account is removed, the ticket survives, just unassigned.
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )

    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.NEW
    )
    priority = models.CharField(
        max_length=6, choices=Priority.choices, default=Priority.MEDIUM
    )

    # Timestamps: auto_now_add sets creation time once; auto_now updates on
    # every save. resolved_at is filled in when the ticket is resolved.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]  # Newest tickets first.

    def __str__(self):
        return f"#{self.pk} {self.title}"


class Comment(models.Model): # A message on a ticket's conversation thread

    # Foreign Key: the ticket this comment belongs to. CASCADE - deleting a ticket
    # removes its comments too.
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    # FK: who wrote the comment.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    body = models.TextField()

    # Internal notes are visible only to agents/admins, never to the end user
    # who raised the ticket. This visibility rule is part of access control.
    is_internal = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]  # Oldest first, so the thread reads top-to-bottom.

    def __str__(self):
        return f"Comment by {self.author} on ticket #{self.ticket_id}"