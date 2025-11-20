from django.urls import path
from . import views

app_name = "patients"

urlpatterns = [
    path("", views.patient_list_view, name="patient-list"),
    path("<int:pk>/", views.patient_detail_view, name = "patient-detail"),
    path("new/", views.patient_create_view, name="patient-create")
]