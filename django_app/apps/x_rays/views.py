from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import XRaysExamination
from .forms import XRaysForm

@login_required
def x_rays_list_view(request):

    context = {
        "app": "x_rays",
        "model": "XRaysExamination",
        "search_fields": [
            {
                "id": "search__patient__full_name",
                "placeholder": "Patient",
            }, {
                "id": "search__examination",
                "placeholder": "Examination",
            }
        ],
        "url_create": "x_rays:x-rays-create",
    }

    return render(request, "digital_clinic/list_view.html", context)

@login_required
def x_rays_detail_view(request, pk):

    obj = get_object_or_404(XRaysExamination, pk = pk)   
    
    context = {
        "app": "x_rays",
        "obj": obj,
        "buttons": {
            "back": "x_rays:x-rays-list",
            "edit": "x_rays:x-rays-update",
            "cp": "x_rays:x-rays-copy",
            "delete": "x_rays:x-rays-delete",
        }
    }
    
    return render(request, "x_rays/x_rays_detail.html", context)


class XRaysCreateView(LoginRequiredMixin, CreateView):
    model = XRaysExamination
    form_class = XRaysForm
    template_name = "x_rays/x_rays_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app"] = "x_rays"

        return context

class XRaysUpdateView(LoginRequiredMixin, UpdateView):
    model = XRaysExamination
    form_class = XRaysForm
    template_name = "x_rays/x_rays_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app"] = "x_rays"

        return context

@login_required
def x_rays_delete_view(request, pk):

    obj = get_object_or_404(XRaysExamination, pk=pk)

    if request.method == "POST":
        obj.delete()
        return redirect("x_rays:x-rays-list")
    
    context = {
        "app": "x_rays",
        "title": "X-Rays Examination",
        "obj": obj,
        "url_detail": "x_rays:x-rays-detail",
    }

    return render(request, "digital_clinic/delete_view.html", context)

@login_required
def x_rays_copy(request, pk):
    obj = get_object_or_404(XRaysExamination, pk=pk)

    fields = {
        field.name: getattr(obj, field.name)
        for field in obj._meta.fields
        if field != "id"
    }

    form = XRaysForm(fields)

    context = {
        "app": "x_rays",
        "form": form
    }

    return render(request, "x_rays/x_rays_form.html", context)
