from django.urls import path

from . import views

app_name = "tickets"  # Namespaces these routes

urlpatterns = [
    path("", views.TicketListView.as_view(), name="list"),
    path("<int:pk>/", views.TicketDetailView.as_view(), name="detail"),
]