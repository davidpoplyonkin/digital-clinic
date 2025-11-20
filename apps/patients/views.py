from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Patient

def patient_list_view(request):    
    search = request.GET.get("search")
    if search:
        results = Patient.objects.filter(full_name__icontains = search) 
    else:
        search = ""
        results = Patient.objects.all()

    paginator = Paginator(results.order_by("full_name"), per_page = 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "app": "patients",
        "search": search,
        "search_placeholder": "Patient Name",
        "url_create": "patients:patient-create",
        "url_this": "patients:patient-list",
        "page_obj": page_obj,
    }

    return render(request, "patients/patient_list.html", context)

def patient_detail_view(request):
    pass

def patient_create_view(request):
    pass
