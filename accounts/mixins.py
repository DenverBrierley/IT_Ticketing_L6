from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin):
    #Restrict a view to users whose role is in `allowed_roles`.

    allowed_roles = ()  # Subclasses or views set this

    def dispatch(self, request, *args, **kwargs):
        # LoginRequiredMixin handle the redirect to login.
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        # Logged in but role not allowed = 403 Forbidden.
        if self.allowed_roles and request.user.role not in self.allowed_roles:
            raise PermissionDenied("You do not have permission to view this page.")
        return super().dispatch(request, *args, **kwargs)


class SupportStaffRequiredMixin(RoleRequiredMixin):
    #Allow only agents and admins 
    allowed_roles = ("AGENT", "ADMIN")


class AdminRequiredMixin(RoleRequiredMixin):
    #Allow only administrators
    allowed_roles = ("ADMIN",)


class OwnerOrStaffRequiredMixin:
    #Object-level check: only the record's owner, or support staff, may access it.


    owner_field = "created_by"  # The model attribute holding the owning user.

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)  # Normal lookup (404 if not found).
        user = self.request.user
        if user.is_support_staff:
            return obj  # Agents/admins may access any record.
        if getattr(obj, self.owner_field) != user:
            # Logged-in, but trying to reach someone else's record.
            raise PermissionDenied("You can only access your own tickets.")
        return obj