from django.urls import path

from . import views

app_name = "custom_fields"

urlpatterns = [
    path("htmx/autocomplete/<str:field>/", views.autocomplete_update, name = "autocomplete-update"),
    path("htmx/autocomplete/<str:field>/<str:direction>/", views.autocomplete_navigate, name = "autocomplete-navigate"),
]