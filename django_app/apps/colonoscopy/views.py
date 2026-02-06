from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
    pass

@login_required
def colonoscopy_create_view(request):
    pass