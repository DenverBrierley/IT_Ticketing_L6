import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_ticket_list_requires_login(client):
    """Anonymous users are redirected to login."""
    response = client.get(reverse("tickets:list"))
    assert response.status_code == 302
    assert "/login/" in response.url


@pytest.mark.django_db
def test_end_user_sees_only_own_tickets(client, end_user, other_user, category):
    """The list view must be scoped to the requesting user's own tickets."""
    from tickets.models import Ticket
    mine = Ticket.objects.create(title="Mine", description="x",
                                 category=category, created_by=end_user)
    theirs = Ticket.objects.create(title="Theirs", description="y",
                                   category=category, created_by=other_user)
    client.force_login(end_user)
    response = client.get(reverse("tickets:list"))
    tickets = list(response.context["tickets"])
    assert mine in tickets
    assert theirs not in tickets


@pytest.mark.django_db
def test_agent_sees_all_tickets(client, agent, end_user, category):
    """Agents see every ticket, not just their own."""
    from tickets.models import Ticket
    Ticket.objects.create(title="Someone's", description="x",
                          category=category, created_by=end_user)
    client.force_login(agent)
    response = client.get(reverse("tickets:list"))
    assert len(response.context["tickets"]) == 1


@pytest.mark.django_db
def test_only_admin_can_delete_ticket(client, end_user, ticket):
    """An end user must not be able to delete a ticket (403)."""
    client.force_login(end_user)
    response = client.get(reverse("tickets:delete", kwargs={"pk": ticket.pk}))
    assert response.status_code == 403