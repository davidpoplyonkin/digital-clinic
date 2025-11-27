from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Lab

@login_required
def lab_list_view(request):
    search = request.GET.get("search")

    if search:
        results = Lab.objects.filter(patient__full_name__icontains = search) 

    else:
        search = ""
        results = Lab.objects.all()

    paginator = Paginator(results.order_by("-date"), per_page = 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "app": "lab",
        "search": search,
        "search_placeholder": "Patient Name",
        "url_create": "lab:lab-create",
        "url_this": "lab:lab-list",
        "page_obj": page_obj,
    }

    return render(request, "lab/lab_list.html", context)

@login_required
def lab_detail_view(request):
    pass

@login_required
def lab_upsert_view(request):
    pass

@login_required
def lab_delete_view(request):
    pass
