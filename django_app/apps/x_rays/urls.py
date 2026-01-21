from django.urls import path

from . import views

app_name = "x_rays"

urlpatterns = [
    path("", views.x_rays_list_view, name="x-rays-list"),
    path("<int:pk>/", views.x_rays_detail_view, name="x-rays-detail"),
    path("new/", views.x_rays_create_view, name="x-rays-create"),
]