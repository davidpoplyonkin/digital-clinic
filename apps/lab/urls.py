from django.urls import path

from . import views

app_name = "lab"

urlpatterns = [
    path("", views.lab_list_view, name="lab-list"),
    path("<int:pk>/", views.lab_detail_view, name="lab-detail"),
    path("new/", views.lab_upsert_view, name="lab-create"),
    path("<int:pk>/update/", views.lab_upsert_view, name="lab-update"),
    path("<int:pk>/delete/", views.lab_delete_view, name="lab-delete"),
]