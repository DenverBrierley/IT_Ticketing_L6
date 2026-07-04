import pytest
from django.utils import timezone

from tickets.models import Ticket


@pytest.mark.django_db
def test_ticket_defaults(ticket):
    """A new ticket should default to NEW status and MEDIUM priority."""
    assert ticket.status == Ticket.Status.NEW
    assert ticket.priority == Ticket.Priority.MEDIUM
    assert ticket.resolved_at is None


@pytest.mark.django_db
def test_ticket_str(ticket):
    """__str__ should include the id and title."""
    assert str(ticket) == f"#{ticket.pk} {ticket.title}"


@pytest.mark.django_db
def test_user_role_properties(agent, admin_user, end_user):
    """Role convenience properties should reflect the assigned role."""
    assert agent.is_agent
    assert agent.is_support_staff
    assert admin_user.is_administrator
    assert admin_user.is_support_staff
    assert not end_user.is_support_staff


@pytest.mark.django_db
def test_category_str(category):
    assert str(category) == "Network"