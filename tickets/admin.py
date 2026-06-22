from django.contrib import admin

from .models import Category, Ticket, Comment


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # Show the most useful columns in the ticket list view.
    list_display = ("id", "title", "category", "status", "priority", "assigned_to")
    list_filter = ("status", "priority", "category")  # Sidebar filters.
    search_fields = ("title", "description")           # Search box.


# Categories and comments use the default admin.
admin.site.register(Category)
admin.site.register(Comment)