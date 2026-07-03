from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Add custom fields to the change/edit form, appended to the default
    # fieldsets to keep everything UserAdmin already provides.
    fieldsets = UserAdmin.fieldsets + (
        ("Helpdesk role", {"fields": ("role", "department")}),
    )
    # expose them when creating a user via the admin "Add" form.
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Helpdesk role", {"fields": ("role", "department")}),
    )
    # Show role in the user list and allow filtering by it.
    list_display = ("username", "email", "role", "is_staff")
    list_filter = UserAdmin.list_filter + ("role",)