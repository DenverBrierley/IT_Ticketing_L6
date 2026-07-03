from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from accounts.mixins import OwnerOrStaffRequiredMixin, AdminRequiredMixin
from .forms import TicketCreateForm, TicketStaffForm
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
    
class TicketCreateView(LoginRequiredMixin, CreateView):
    """Raise a new ticket. Any logged-in user may create one."""

    model = Ticket
    form_class = TicketCreateForm
    template_name = "tickets/ticket_form.html"

    def form_valid(self, form):
        # Set the owner from the logged-in user server-side — never trust the
        # browser to tell us who created the ticket.
        form.instance.created_by = self.request.user
        messages.success(self.request, "Ticket raised successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tickets:detail", kwargs={"pk": self.object.pk})


class TicketUpdateView(OwnerOrStaffRequiredMixin, LoginRequiredMixin, UpdateView):
    """Edit a ticket.

    Owners and staff may reach it (ownership enforced by the mixin). The FORM
    chosen depends on role: staff get the fuller triage form; end users get the
    limited one, so they can't change status/assignee even here.
    """

    model = Ticket
    template_name = "tickets/ticket_form.html"

    def get_form_class(self):
        return TicketStaffForm if self.request.user.is_support_staff else TicketCreateForm

    def form_valid(self, form):
        # Stamp the resolution time when a ticket is first marked resolved.
        if form.instance.status == Ticket.Status.RESOLVED and not form.instance.resolved_at:
            form.instance.resolved_at = timezone.now()
        messages.success(self.request, "Ticket updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tickets:detail", kwargs={"pk": self.object.pk})


class TicketDeleteView(AdminRequiredMixin, DeleteView):
    #Delete a ticket. Admin-only, and requires confirmation first

    model = Ticket
    template_name = "tickets/ticket_confirm_delete.html"
    success_url = reverse_lazy("tickets:list")

    def form_valid(self, form):
        messages.success(self.request, "Ticket deleted.")
        return super().form_valid(form)