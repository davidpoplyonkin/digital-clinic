from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.apps import apps

@login_required
def autocomplete_update(request, field):
    """
    Resets the counter when the user resumes typing.
    """

    context = {
        "field": field,
        "ac_text": request.POST.get(field),
        "ac_counter": 0, # reset the counter
        "ac_search_field": request.POST.get(f"{field}_ac_search_field"),
        "label": request.POST.get(f"{field}_label"),
        "app": request.POST.get(f"{field}_app"),
        "model": request.POST.get(f"{field}_model"),
        "on_load_post": request.POST.get(f"{field}_on_load_post"),
    }

    return render(request, "core/partials/autocomplete.html", context)

@login_required
def autocomplete_navigate(request, field, direction):
    """
    Updates the counter after the user presses the up or down arrow.
    Then, returns the search result at the position equal to the
    counter's value.
    """

    ac_counter = int(request.POST.get(f"{field}_ac_counter"))

    if ac_counter != 0:
        ac_query = request.POST.get(f"{field}_ac_query")
    else:
        ac_query = request.POST.get(field)

    model = apps.get_model(
        request.POST.get(f"{field}_app"),
        request.POST.get(f"{field}_model")
    )

    ac_search_field = request.POST.get(f"{field}_ac_search_field")
    ac_query_kwargs = {
        f"{ac_search_field}__icontains": ac_query,
        f"{ac_search_field}__gt": "",
    }

    # Take the objects whose name matches the query.
    obj = model.objects.filter(**ac_query_kwargs)

    # Take the names of these objects
    options = obj.values_list(ac_search_field, flat = True)

    # Prepend the query to the list.
    options = [ac_query] + list(options)

    # Determine which of the suggested names to return to the user.
    if direction == "up":
        ac_counter -= 1
    else:
        ac_counter += 1

    ac_counter = ac_counter % len(options)

    context = {
        "field": field,
        "ac_text": options[ac_counter],
        "ac_counter": ac_counter,
        "ac_query": ac_query,
        "ac_search_field": ac_search_field,
        "label": request.POST.get(f"{field}_label"),
        "app": request.POST.get(f"{field}_app"),
        "model": request.POST.get(f"{field}_model"),
        "on_load_post": request.POST.get(f"{field}_on_load_post"),
    }
    
    # NOTE: If the new piece of text is longer than the previous one,
    # the cursor might end up in the middle of it. However, this is ok
    # given that the user is not supposed to type anything after they
    # find the correct name.

    return render(request, "core/partials/autocomplete.html", context)

# HTMX
@login_required
def list_search(request):
    """
    Given the search query and the page, populates the list view with
    content.
    """

    app = request.POST.get("app")
    model = request.POST.get("model")
    page = request.POST.get("page")

    search_kwargs = {
        (k.split("__", 1)[1] + "__icontains"): v # "search__field" -> "field__icontains"
        for k, v in request.POST.items()
        if k.startswith("search__")
    }

    try:
        results = apps.get_model(app, model).objects.filter(**search_kwargs)
    except:
        results = None

    if results:
        paginator = Paginator(results, per_page = 10)
        page_obj = paginator.get_page(page)
    else:
        page_obj = None

    context = {
        "app": app,
        "model": model,
        "page_obj": page_obj,
    }
    
    return render(request, f"{app}/list_table.html", context)
