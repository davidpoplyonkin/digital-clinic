from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Panel

@login_required
def panel_list_view(request):
    search = request.GET.get("search")

    if search:
        results = Panel.objects.filter(name__icontains = search)

    else:
        search = ""
        results = Panel.objects.all()

    paginator = Paginator(results.order_by("name"), per_page = 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "app": "panels",
        "search": search,
        "search_placeholder": "Panel Name",
        "url_create": "panels:panel-create",
        "url_this": "panels:panel-list",
        "page_obj": page_obj,
    }

    return render(request, "panels/panel_list.html", context)

@login_required
def panel_detail_view(request):
    pass

@login_required
def panel_upsert_view(request):
    pass

@login_required
def panel_delete_view(request):
    pass