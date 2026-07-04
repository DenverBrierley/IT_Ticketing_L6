from django.urls import path

from . import views
from . import management_views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("users/", management_views.UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/edit/", management_views.UserManageView.as_view(), name="user_manage"),
]