from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Test, TestAgeGroup

@login_required
def test_list_view(request):
    search = request.GET.get("search")
    if search:
        results = Test.objects.filter(name__icontains = search)
    else:
        search = ""
        results = Test.objects.all()

    paginator = Paginator(results.order_by("name"), per_page = 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "app": "tests",
        "search": search,
        "search_placeholder": "Test Name",
        "url_create": "tests:test-create",
        "url_this": "tests:test-list",
        "page_obj": page_obj,
    }

    return render(request, "tests/test_list.html", context)

@login_required
def test_detail_view(request, pk):

    test = get_object_or_404(Test, pk = pk)
    age_groups = TestAgeGroup.objects.filter(test = test)
    
    context = {
        "app": "tests",
        "obj": test,
        "age_groups": age_groups,
        "additional_buttons": [
            {
                "url": "tests:test-update",
                "bootstrap_class": "btn-outline-secondary",
                "bootstrap_icon": "bi-pencil",
                "text": "Edit",
            }, {
                "url": "tests:test-delete",
                "bootstrap_class": "btn-outline-danger",
                "bootstrap_icon": "bi-trash",
                "text": "Delete",
            }
        ],
        "url_list": "tests:test-list",
    }
    
    return render(request, "tests/test_detail.html", context)

@login_required
def test_upsert_view(request):
    pass

@login_required
def test_delete_view(request):
    pass
