
from django import forms

from .models import Ticket


class TicketCreateForm(forms.ModelForm):
   #Used by end users to raise a ticket.
    #Only these three fields are editable. created_by is set in the view (never
    #trusted from the browser), and status/priority/assignee use their defaults.
    

    class Meta:
        model = Ticket
        fields = ("title", "description", "category")

    def clean_title(self):
        # Extra server-side validation beyond the field's max_length.
        title = self.cleaned_data["title"].strip()
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters.")
        return title


class TicketStaffForm(forms.ModelForm):
    #Used by agents/admins to triage: they can also set status, priority,
    #and reassign the ticket.

    class Meta:
        model = Ticket
        fields = ("title", "description", "category",
                  "status", "priority", "assigned_to")