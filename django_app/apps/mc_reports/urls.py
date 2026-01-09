from django.urls import path

from . import views

app_name = "mc_reports"

urlpatterns = [
    path("", views.mcr_list_view, name="mcr-list"),
    path("<int:pk>/", views.mcr_detail_view, name="mcr-detail"),
    path("new/", views.mcr_upsert_view, name="mcr-create"),
    path("<int:pk>/update/", views.mcr_upsert_view, name="mcr-update"),
    path("<int:pk>/delete/", views.mcr_delete_view, name="mcr-delete"),
]