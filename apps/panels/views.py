from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import re

from .models import Panel, PanelTest
from ..tests.models import Test
from .forms import PanelForm, PanelTestFormSet

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
def panel_upsert_view(request, pk = None):
    if pk is None:
        panel = None
    else:
        panel = get_object_or_404(Panel, pk = pk)

    form = PanelForm(instance = panel)
    formset = PanelTestFormSet(instance = panel)

    if request.method == "POST":
        form = PanelForm(request.POST, instance = panel)
        formset = PanelTestFormSet(request.POST, instance = panel)
        
        if form.is_valid():
            panel = form.save(commit = False)
            formset = PanelTestFormSet(request.POST, instance = panel)

            if formset.is_valid():
                form.save()
                formset.save()
                return redirect(reverse("panels:panel-detail", kwargs={"pk": panel.pk}))
        
    formset.is_valid() # force lookup/hydration of Test instances
    
    # If there was an error, and the formset is returned to the user,
    # the forms need to be sorted
    formset.forms = sorted(
        formset.forms,
        key = lambda form: getattr(form.instance, "order", 0),
        reverse = False
    )

    return render(request, "panels/panel_form.html", {
        "form": form,
        "formset": formset,
    })

@login_required
def panel_delete_view(request, pk):

    obj = get_object_or_404(Panel, pk = pk)

    if request.method == "POST":
        obj.delete()
        return redirect("panels:panel-list")
    
    context = {
        "title": "Panel",
        "obj": obj,
        "url_detail": "panels:panel-detail",
    }

    return render(request, "digital_clinic/delete_view.html", context)

# HTMX VIEWS
@login_required
def test_search(request):
    """
    Return the results that match the active search query.
    """

    form_data = request.POST
    search_results = []
    pattern = r"^paneltest_set-[0-9]+-test$"
    tests_disabled = []

    # Find the tests that are already in the list, and thus should
    # appear disabled it test search results.
    for key, value in form_data.items():
        if re.match(pattern, key):
            pt_prefix = key[:-5]

            # Make sure that the test is actually in the list, rather than
            # among the deleted forms.
            if (f"{pt_prefix}-DELETE" not in form_data.keys()):
                tests_disabled.append(int(value))

    # Iterate over all tests that match the query.
    for test in Test.objects.filter(
            name__icontains = request.POST.get("search")
    ):
        search_results.append({
            "pk": test.pk,
            "name": test.name,
            "is_disabled": bool(test.pk in tests_disabled)
        })

    return render(
        request,
        "panels/partials/test_search.html",
        {"search_results": search_results}
    )

@login_required  
def paneltest_sort(request):
    """
    After the forms are swapped on the client side, this updates the
    the "Order" field to match the new order of the forms.
    """

    form_data = request.POST
    pattern = r"^paneltest_set-[0-9]+-order$"
    paneltest_rows = []
    i = 1
    
    # Iterate over the "Order" field in the order it appears in the
    # POST request (i.e. the order it appears on the client side).
    for key in form_data.keys():
        if re.match(pattern, key):
            paneltest_rows.append({
                "order_name": key,
                "order_value": i
            })
            i += 1
        
    return render(
        request,
        "panels/partials/paneltest_sort.html",
        {"paneltest_rows": paneltest_rows}
    )

@login_required
def paneltest_append(request, test_pk):
    """
    After the user clicks on a test below the test search, this appends
    a newly-created paneltest form to the list.
    """

    form_data = request.POST
    test_pattern = r"^paneltest_set-[0-9]+-test$"
    order_pattern = r"^paneltest_set-[0-9]+-order$"
    context = {}
    paneltest_prefix = ""
    num_forms = 0
    max_prefix = -1 # inner formset index of the form

    # Find a formset form that is connected to the `pk` Test.
    for key, value in form_data.items():

        # All forms: visible or not, newly-created or not - are
        # guaranteed to have the test field.
        if re.match(test_pattern, key):

            if value == str(test_pk):
                paneltest_prefix = key[:-5]
                context["prefix"] = paneltest_prefix
                break

            # Identify the next formset form prefix in case none of the
            # existing ones is connected to `pk`.
            max_prefix = max(
                max_prefix,
                int(key[14:-5]) # [0-9]+ part in `test_pattern`
            )
    
    # If there is no `pk` Test in the list ...
    if paneltest_prefix == "":
        context["prefix"] = f"paneltest_set-{max_prefix + 1}"
        context["total_forms"] = int(form_data["paneltest_set-TOTAL_FORMS"]) + 1

    else:
        # If the test was deleted and is now prepended to the list ...
        if f"{paneltest_prefix}-DELETE" in form_data.keys(): 
            context["paneltest_pk"] = form_data[f"{paneltest_prefix}-id"]
        else:
            return HttpResponse("") # don't do anything
    
    # Count how many visible forms are there.
    for key, value in form_data.items():
        if re.match(order_pattern, key):
            tmp_prefix = key[:-6]
            if f"{tmp_prefix}-DELETE" not in form_data.keys():
                num_forms += 1

    context["test_pk"] = test_pk
    context["test_name"] = Test.objects.filter(pk = test_pk)[0].name
    context["order"] = num_forms + 1

    return render(request, "panels/partials/paneltest_append.html", context)

@login_required
def paneltest_delete(request, prefix):
    form_data = request.POST
    context = {}

    # If this is a newly-created form, there is no need to prepend it -
    # just decrement the total number of forms.
    if f"{prefix}-id" not in form_data.keys():
        context["total_forms"] = int(form_data["paneltest_set-TOTAL_FORMS"]) - 1

    # Otherwise, make the form invisible since the formset still needs
    # to know that it has to be deleted.
    else:
        context["paneltest_pk"] = form_data[f"{prefix}-id"]
        context["test_pk"] = form_data[f"{prefix}-test"]

    context["del"] = "on"
    context["prefix"] = prefix
    
    # The deleted forms are placed in a separate list because if the
    # first row in a Bootstrap list-group has style="display: none",
    # the upper border also becomes invisible
    return render(request, "panels/partials/paneltest_delete.html", context)