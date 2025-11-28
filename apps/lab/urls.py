from django.urls import path

from . import views

app_name = "lab"

urlpatterns = [
    path("", views.lab_list_view, name="lab-list"),
    path("<int:pk>/", views.lab_detail_view, name="lab-detail"),
    path("new/", views.LabWizardView.as_view(), name="lab-create"),
    path("<int:pk>/update/", views.LabWizardView.as_view(), name="lab-update"),
    path("<int:pk>/delete/", views.lab_delete_view, name="lab-delete"),
    path("<int:pk>/print/", views.lab_print, name="lab-print"),

    # HTMX
    path("htmx/new/testresult/update", views.LabWizardView.as_view(), name="lab-create-testresult-update"),
    path("htmx/<int:pk>/testresult/update", views.LabWizardView.as_view(), name="lab-update-testresult-update"),
]