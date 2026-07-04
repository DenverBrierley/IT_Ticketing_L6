from django.urls import path

from . import views
from . import category_views 

app_name = "tickets"  # Namespaces these routes

urlpatterns = [
    path("", views.TicketListView.as_view(), name="list"),
    path("new/", views.TicketCreateView.as_view(), name="create"),
    path("<int:pk>/", views.TicketDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.TicketUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.TicketDeleteView.as_view(), name="delete"),
       # Admin-only category management.
    path("categories/", category_views.CategoryListView.as_view(), name="category_list"),
    path("categories/new/", category_views.CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/edit/", category_views.CategoryUpdateView.as_view(), name="category_update"),
    path("categories/<int:pk>/delete/", category_views.CategoryDeleteView.as_view(), name="category_delete"),
]