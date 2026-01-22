from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import XRaysExamination

@login_required
def x_rays_list_view(request):

    context = {
        "app": "x_rays",
        "model": "XRaysExamination",
        "search_fields": [
            {
                "id": "search__patient__full_name",
                "placeholder": "Patient",
            }, {
                "id": "search__examination",
                "placeholder": "Examination",
            }
        ],
        "url_create": "x_rays:x-rays-create",
    }

    return render(request, "digital_clinic/list_view.html", context)

@login_required
def x_rays_detail_view(request, pk):
    pass

@login_required
def x_rays_create_view(request):
    pass
