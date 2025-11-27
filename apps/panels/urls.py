from django.urls import path
from . import views

app_name = "panels"

urlpatterns = [
    path("", views.panel_list_view, name="panel-list"),
    path("<int:pk>/", views.panel_detail_view, name="panel-detail"),
    path("new/", views.panel_upsert_view, name="panel-create"),
    path("<int:pk>/update/", views.panel_upsert_view, name="panel-update"),
    path("<int:pk>/delete/", views.panel_delete_view, name="panel-delete"),

    # HTMX
    path("htmx/test/search/", views.test_search, name="test-search"),
    path("htmx/paneltest/sort/", views.paneltest_sort, name="paneltest-sort"),
    path("htmx/paneltest/<int:test_pk>/append/", views.paneltest_append, name="paneltest-append"),
    path("htmx/paneltest/<str:prefix>/delete/", views.paneltest_delete, name="paneltest-delete"),
]