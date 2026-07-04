from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from .mixins import AdminRequiredMixin
from .models import User
from .admin_forms import UserManageForm

"""
Admin-only views for managing users: list all users and edit a user's role,
department, and active status.
"""

class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "users"
    ordering = ("username",)


class UserManageView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserManageForm
    template_name = "accounts/user_manage.html"
    success_url = reverse_lazy("accounts:user_list")

    def form_valid(self, form):
        messages.success(self.request, "User updated.")
        return super().form_valid(form)