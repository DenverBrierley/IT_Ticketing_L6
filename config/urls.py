from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views as account_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Custom registration view.
    path("register/", account_views.register, name="register"),

    # built-in login/logout views handle the secure session work.
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]