from django.urls import path
from . import views

app_name = "tests"

urlpatterns = [
    path("", views.test_list_view, name="test-list"),
    path("<int:pk>/", views.test_detail_view, name="test-detail"),
    path("new/", views.test_upsert_view, name="test-create"),
    path("<int:pk>/update/", views.test_upsert_view, name="test-update"),
    path("<int:pk>/delete/", views.test_delete_view, name="test-delete"),

    # HTMX
    path("htmx/agegroup/new/", views.agegroup_append, name="agegroup-append"),
    path("htmx/agegroup/<str:prefix>/delete/", views.agegroup_delete, name="agegroup-delete"),
]
