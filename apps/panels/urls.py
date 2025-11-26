from django.urls import path
from . import views

app_name = "panels"

urlpatterns = [
    path("", views.panel_list_view, name="panel-list"),
    path("<int:pk>/", views.panel_detail_view, name="panel-detail"),
    path("new/", views.panel_upsert_view, name="panel-create"),
    path("<int:pk>/update/", views.panel_upsert_view, name="panel-update"),
    path("<int:pk>/delete/", views.panel_delete_view, name="panel-delete"),
]