from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from accounts import views as account_views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="tickets:list"), name="home"),
    path("admin/", admin.site.urls),

    # Custom registration view.
    path("register/", account_views.register, name="register"),

    #register and user management
    path("accounts/", include("accounts.urls")), 

    # built-in login/logout views handle the secure session work.
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("tickets/", include("tickets.urls")),
]