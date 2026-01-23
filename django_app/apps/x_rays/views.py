from django.shortcuts import render, get_object_or_404
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
        "app": "patients",
        "obj": obj,
        "buttons": {
            "back": "x_rays:x-rays-list",
            "edit": "x_rays:x-rays-update",
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
