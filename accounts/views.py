from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import RegisterForm


def register(request):
    """Handle new-user sign-up.

    On POST, validate the form; if valid, create the user (password is
    hashed automatically by the form), log them in, and redirect. On GET,
    show a blank form.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the new user straight in.
            messages.success(request, "Account created — welcome!")
            return redirect("login")  # Temporary target; becomes the dashboard in Step 6.
        # Invalid: fall through and re-render with error messages shown.
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})