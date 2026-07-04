from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from tickets.models import Ticket


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Scope the base queryset to what this user may see.
        if user.is_support_staff:
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(created_by=user)

        # Summary counts for the cards.
        context["total"] = tickets.count()
        context["open_count"] = tickets.exclude(
            status__in=[Ticket.Status.RESOLVED, Ticket.Status.CLOSED]
        ).count()
        context["resolved_count"] = tickets.filter(status=Ticket.Status.RESOLVED).count()

        # Agents/admins also get an "unassigned" figure to action.
        if user.is_support_staff:
            context["unassigned_count"] = tickets.filter(assigned_to__isnull=True).count()

        context["recent"] = tickets.select_related("category")[:5]
        return context