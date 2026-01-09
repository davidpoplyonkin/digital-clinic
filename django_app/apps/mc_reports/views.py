from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import MCReport

@login_required
def mcr_list_view(request):

    search = request.GET.get("search")

    if search:
        results = MCReport.objects.filter(patient__full_name__icontains = search) 

    else:
        search = ""
        results = MCReport.objects.all()

    paginator = Paginator(results.order_by("-date"), per_page = 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "app": "mc_reports",
        "search": search,
        "search_placeholder": "Patient Name",
        "url_create": "mc_reports:mcr-create",
        "url_this": "mc_reports:mcr-list",
        "page_obj": page_obj,
    }

    return render(request, "mc_reports/mcr_list.html", context)

@login_required
def mcr_detail_view(request):
    pass

@login_required
def mcr_upsert_view(request):
    pass

@login_required
def mcr_delete_view(request):
    pass
