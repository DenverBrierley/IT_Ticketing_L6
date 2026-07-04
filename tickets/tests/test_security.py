import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_user_cannot_access_others_ticket(client, other_user, ticket):
    """A01: a logged-in user cannot open another user's ticket by URL (403)."""
    client.force_login(other_user)  # ticket is owned by end_user, not this one
    response = client.get(reverse("tickets:detail", kwargs={"pk": ticket.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_comment_body_is_escaped(client, end_user, ticket):
    """A03/XSS: a script tag in a comment is escaped, not rendered raw."""
    client.force_login(end_user)
    payload = "<script>alert('xss')</script>"
    client.post(reverse("tickets:detail", kwargs={"pk": ticket.pk}),
                {"body": payload})
    response = client.get(reverse("tickets:detail", kwargs={"pk": ticket.pk}))
    content = response.content.decode()
    # The raw script tag must NOT appear; its escaped form should.
    assert "<script>alert('xss')</script>" not in content
    assert "&lt;script&gt;" in content


@pytest.mark.django_db
def test_weak_password_rejected(client):
    """A07: registration rejects a weak, common password."""
    response = client.post(reverse("accounts:register"), {
        "username": "newperson",
        "password1": "password",   # deliberately weak/common
        "password2": "password",
    })
    # Form re-renders (200) with errors rather than redirecting on success.
    assert response.status_code == 200
    assert b"too common" in response.content or b"too short" in response.content