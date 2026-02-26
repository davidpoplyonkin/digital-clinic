from django.urls import path

from . import views

app_name = "colonoscopy"

urlpatterns = [
    path("", views.colonoscopy_list_view, name="colonoscopy-list"),
    path("<int:pk>/", views.colonoscopy_detail_view, name="colonoscopy-detail"),
    path("new/", views.ColonoscopyWizardView.as_view(), name="colonoscopy-create"),
    path(
        "<int:pk>/update/",
        views.ColonoscopyWizardView.as_view(),
        name="colonoscopy-update",
    ),
    # HTMX
    path("htmx/image/new/", views.image_append, name="image-append"),
]
