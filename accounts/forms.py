from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    """Sign-up form for new end users.

    Extends UserCreationForm, which enforces password
    confirmation and runs the configured password-strength validators. new
    accounts default to the USER role, so the role is
    never chosen by user.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")