from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Lab, TestResult

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
def lab_detail_view(request, pk):
    lab = get_object_or_404(Lab, pk = pk)
    res = (
        TestResult.objects
        .filter(lab = lab)
        .select_related("test")
    )
    
    context = {
        "app": "lab",
        "obj": lab,
        "res": res,
        "additional_buttons": [
            {
                "url": "lab:lab-update",
                "bootstrap_class": "btn-outline-secondary",
                "bootstrap_icon": "bi-pencil",
                "text": "Edit",
            }, {
                "url": "lab:lab-delete",
                "bootstrap_class": "btn-outline-danger",
                "bootstrap_icon": "bi-trash",
                "text": "Delete",
            }
        ],
        "url_list": "lab:lab-list"
    }
    
    return render(request, "lab/lab_detail.html", context)

@login_required
def lab_upsert_view(request):
    pass

@login_required
def lab_delete_view(request):
    pass
