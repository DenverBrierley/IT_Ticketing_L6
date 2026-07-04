import pytest
from django.contrib.auth import get_user_model

from tickets.models import Category, Ticket

User = get_user_model()


@pytest.fixture(autouse=True)
def disable_axes(settings):
    # Turn off brute-force lockout during tests so auth tests aren't blocked.
    settings.AXES_ENABLED = False


@pytest.fixture
def end_user(db):
    return User.objects.create_user(
        username="enduser", password="Testpass123!", role="USER"
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username="otheruser", password="Testpass123!", role="USER"
    )


@pytest.fixture
def agent(db):
    return User.objects.create_user(
        username="agent", password="Testpass123!", role="AGENT"
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        username="adminuser", password="Testpass123!", role="ADMIN"
    )


@pytest.fixture
def category(db):
    return Category.objects.create(name="Network", description="Connectivity")


@pytest.fixture
def ticket(db, end_user, category):
    # A ticket owned by end_user.
    return Ticket.objects.create(
        title="Test ticket for suite",
        description="A description.",
        category=category,
        created_by=end_user,
    )