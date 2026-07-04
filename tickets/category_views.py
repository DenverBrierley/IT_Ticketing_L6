from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.shortcuts import redirect

from django.db.models import ProtectedError

from accounts.mixins import AdminRequiredMixin
from .models import Category
"""
Admin-only CRUD views for ticket categories.

All views require the ADMIN role via AdminRequiredMixin, which returns 403
for anyone else — enforcing access control at the view layer.
"""

class CategoryListView(AdminRequiredMixin, ListView):
    model = Category
    template_name = "tickets/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(AdminRequiredMixin, CreateView):
    model = Category
    fields = ("name", "description")
    template_name = "tickets/category_form.html"
    success_url = reverse_lazy("tickets:category_list")

    def form_valid(self, form):
        messages.success(self.request, "Category created.")
        return super().form_valid(form)


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = Category
    fields = ("name", "description")
    template_name = "tickets/category_form.html"
    success_url = reverse_lazy("tickets:category_list")

    def form_valid(self, form):
        messages.success(self.request, "Category updated.")
        return super().form_valid(form)


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    model = Category
    template_name = "tickets/category_confirm_delete.html"
    success_url = reverse_lazy("tickets:category_list")

    def post(self, request, *args, **kwargs):
        # Attempt deletion, but catch the case where tickets still reference
        # this category (on_delete=PROTECT) and show a message
        # instead of a 500 error.
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "Category deleted.")
            return response
        except ProtectedError:
            messages.error(
                request,
                "Cannot delete this category because tickets are using it.",
            )
            return redirect("tickets:category_list")