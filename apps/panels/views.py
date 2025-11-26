from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Panel, PanelTest

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
def panel_detail_view(request, pk):

    panel = get_object_or_404(Panel, pk = pk)
    panel_tests = PanelTest.objects.filter(panel = panel)
    
    context = {
        "app": "panels",
        "obj": panel,
        "panel_tests": panel_tests,
        "additional_buttons": [
            {
                "url": "panels:panel-update",
                "bootstrap_class": "btn-outline-secondary",
                "bootstrap_icon": "bi-pencil",
                "text": "Edit",
            }, {
                "url": "panels:panel-delete",
                "bootstrap_class": "btn-outline-danger",
                "bootstrap_icon": "bi-trash",
                "text": "Delete",
            }
        ],
        "url_list": "panels:panel-list"
    }
    
    return render(request, "panels/panel_detail.html", context)

@login_required
def panel_upsert_view(request):
    pass

@login_required
def panel_delete_view(request):
    pass