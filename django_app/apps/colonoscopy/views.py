from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import ColonoscopyReport

@login_required
def colonoscopy_list_view(request):
    context = {
        "app": "colonoscopy",
        "model": "ColonoscopyReport",
        "search_fields": [
            {
                "id": "search__patient__full_name",
                "placeholder": "Patient",
            }, {
                "id": "search__procedure",
                "placeholder": "Procedure",
            }
        ],
        "url_create": "colonoscopy:colonoscopy-create",
    }

    return render(request, "digital_clinic/list_view.html", context)

@login_required
def colonoscopy_detail_view(request, pk):
    try:
        obj = (
            ColonoscopyReport.objects
            .prefetch_related("patient", "photoprotocolimage_set")
            .get(pk=pk)
        )
    except ColonoscopyReport.DoesNotExist:
        raise Http404("Colonoscopy report not found")
    
    context = {
        "app": "colonoscopy",
        "obj": obj,
        "buttons": {
            "back": "colonoscopy:colonoscopy-list",
        }
    }
    
    return render(request, "colonoscopy/colonoscopy_detail.html", context)

@login_required
def colonoscopy_create_view(request):
    pass