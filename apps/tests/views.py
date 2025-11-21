from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Test

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
def test_detail_view(request):
    pass

@login_required
def test_upsert_view(request):
    pass

@login_required
def test_delete_view(request):
    pass
