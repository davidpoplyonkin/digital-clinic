from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Test, TestAgeGroup
from .forms import TestForm, TestAgeGroupFormSet

@login_required
def test_list_view(request):

    context = {
        "app": "tests",
        "model": "Test",
        "search_fields": [
            {
                "id": "search__name",
                "placeholder": "Test",
            }
        ],
        "url_create": "tests:test-create",
    }

    return render(request, "digital_clinic/list_view.html", context)

@login_required
def test_detail_view(request, pk):

    test = get_object_or_404(Test, pk = pk)
    age_groups = TestAgeGroup.objects.filter(test = test)
    
    context = {
        "app": "tests",
        "obj": test,
        "age_groups": age_groups,
        "buttons": {
            "back": "tests:test-list",
            "edit": "tests:test-update",
            "delete": "tests:test-delete",
        }
    }
    
    return render(request, "tests/test_detail.html", context)

@login_required
def test_upsert_view(request, pk = None):
    if pk is None:
        test = None
    else:
        test = get_object_or_404(Test, pk = pk)

    form = TestForm(instance = test)
    formset = TestAgeGroupFormSet(instance = test)
    formset_errors = set()

    if request.method == "POST":
        form = TestForm(request.POST, instance = test)
        formset = TestAgeGroupFormSet(request.POST, instance = test)

        if form.is_valid():
            test = form.save(commit = False)
            formset = TestAgeGroupFormSet(request.POST, instance = test)
            
            if formset.is_valid():
                form.save()
                formset.save()

                return redirect(reverse("tests:test-detail", kwargs = {"pk": test.pk}))
        
        # Create a set of formset errors.
        for f in formset:
            for field, errors in f.errors.items():
                for e in errors:

                    # Skip the forms marked for deletion.
                    if f.cleaned_data.get("DELETE"):
                        continue

                    if str(e) == "This field is required.":
                        formset_errors.add("No field can be blank.")
                        continue

                    formset_errors.add(e)

        # Add non-form errors.
        for e in formset.non_form_errors():
            formset_errors.add(e)

    return render(request, "tests/test_form.html", {
        "app": "tests",
        "form": form,
        "formset": formset,
        "formset_errors": formset_errors,
    })

@login_required
def test_delete_view(request, pk):
    obj = get_object_or_404(Test, pk = pk)

    if request.method == "POST":
        obj.delete()
        return redirect("tests:test-list")
    
    context = {
        "app": "tests",
        "title": "Test",
        "obj": obj,
        "url_detail": "tests:test-detail",
    }

    return render(request, "digital_clinic/delete_view.html", context)

# HTMX VIEWS

@login_required
def agegroup_append(request):
    """Append an empty TestAgeGroup form"""
    form_data = request.POST
    context = {}
    max_prefix = -1

    # Find the prefix with the largest number.
    for k in form_data.keys():
        k_segments = k.split("-")

        # No dashes
        if len(k_segments) < 2:
            continue

        if k_segments[0] != "testagegroup_set":
            continue

        try:
            max_prefix = max(max_prefix, int(k_segments[1]))
        except ValueError:
            continue

    context["prefix"] = f"testagegroup_set-{max_prefix + 1}"
    context["total_forms"] = int(form_data["testagegroup_set-TOTAL_FORMS"]) + 1

    return render(request, "tests/partials/agegroup_append.html", context)

@login_required
def agegroup_delete(request, prefix):
    form_data = request.POST
    context = {}

    # If this is a newly-created form, there is no need to prepend it -
    # just decrement the total number of forms.
    if f"{prefix}-id" not in form_data.keys():
        context["total_forms"] = int(form_data["testagegroup_set-TOTAL_FORMS"]) - 1

    # Otherwise, make the form invisible since the formset still needs
    # to know that it has to be deleted.
    else:
        context["agegroup_pk"] = form_data[f"{prefix}-id"]

    context["del"] = "on"
    context["prefix"] = prefix
    
    return render(request, "tests/partials/agegroup_delete.html", context)
