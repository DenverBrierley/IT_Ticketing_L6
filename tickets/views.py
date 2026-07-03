from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from accounts.mixins import OwnerOrStaffRequiredMixin
from .models import Ticket


class TicketListView(LoginRequiredMixin, ListView):
    #List tickets, scoped to what the current user is allowed to see

    model = Ticket
    template_name = "tickets/ticket_list.html"
    context_object_name = "tickets"
    paginate_by = 10  # Keeps long lists manageable.

    def get_queryset(self):
        user = self.request.user
        # Support staff see every ticket
        # end users see only their own.
        if user.is_support_staff:
            qs = Ticket.objects.all()
        else:
            qs = Ticket.objects.filter(created_by=user)
        # pulls category/assignee in one query 
        return qs.select_related("category", "assigned_to", "created_by")


class TicketDetailView(OwnerOrStaffRequiredMixin, LoginRequiredMixin, DetailView):
    #Show a single ticket. Ownership is enforced by the mixin's get_object()

    model = Ticket
    template_name = "tickets/ticket_detail.html"
    context_object_name = "ticket"

    def get_queryset(self):
        # Pre-join related rows for the detail template.
        return Ticket.objects.select_related(
            "category", "assigned_to", "created_by"
        )