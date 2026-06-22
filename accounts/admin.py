from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Register the custom user with Django's built-in UserAdmin so the admin
# keeps secure password handling (hashing and the dedicated change-password
# form) instead of exposing a raw, editable password field.
admin.site.register(User, UserAdmin)