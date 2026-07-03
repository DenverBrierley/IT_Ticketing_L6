from django.urls import path

from . import views

app_name = "tickets"  # Namespaces these routes

urlpatterns = [
    path("", views.TicketListView.as_view(), name="list"),
    path("new/", views.TicketCreateView.as_view(), name="create"),
    path("<int:pk>/", views.TicketDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.TicketUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.TicketDeleteView.as_view(), name="delete"),
]