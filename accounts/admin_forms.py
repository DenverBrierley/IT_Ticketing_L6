from django import forms

from .models import User


class UserManageForm(forms.ModelForm):
    #Lets an administrator change a user's role, department and active state.
    #excludes username/password: this page is for role and access
    #management, not identity or credential changes.

    class Meta:
        model = User
        fields = ("role", "department", "is_active")