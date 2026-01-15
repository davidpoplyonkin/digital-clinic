from django.urls import path

from . import views

app_name = "mc_reports"

urlpatterns = [
    path("", views.mcr_list_view, name="mcr-list"),
    path("<int:pk>/", views.mcr_detail_view, name="mcr-detail"),
    path("new/", views.MCReportCreateView.as_view(), name="mcr-create"),
    path("<int:pk>/update/", views.MCReportUpdateView.as_view(), name="mcr-update"),
    path("<int:pk>/delete/", views.mcr_delete_view, name="mcr-delete"),
    path("<int:pk>/print/", views.mcr_print, name="mcr-print"),
    path("<int:pk>/copy/", views.mcr_copy, name="mcr-copy")
]