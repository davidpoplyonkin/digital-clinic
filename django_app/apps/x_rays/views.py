from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import XRaysExamination

@login_required
def x_rays_list_view(request):

    search = request.GET.get("search")

    if search:
        results = XRaysExamination.objects.filter(patient__full_name__icontains = search) 

    else:
        search = ""
        results = XRaysExamination.objects.all()

    paginator = Paginator(results.order_by("-date"), per_page = 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "app": "x_rays",
        "search": search,
        "search_placeholder": "Patient Name",
        "url_create": "x_rays:x-rays-create",
        "url_this": "x_rays:x-rays-list",
        "page_obj": page_obj,
    }

    return render(request, "x_rays/x_rays_list.html", context)

@login_required
def x_rays_detail_view(request, pk):
    pass

@login_required
def x_rays_create_view(request):
    pass
