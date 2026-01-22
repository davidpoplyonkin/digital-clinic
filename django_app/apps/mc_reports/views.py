from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404

from .models import MCReport
from .forms import MCReportForm

try:
    from .utils.mcr_pdf_generator import generate_pdf
except ModuleNotFoundError:
    from ..core.utils.example_pdf_generator import generate_pdf

@login_required
def mcr_list_view(request):
    context = {
        "app": "mc_reports",
        "model": "MCReport",
        "search_id": "search__patient__full_name",
        "search_placeholder": "Patient Name",
        "url_create": "mc_reports:mcr-create",
    }

    return render(request, "digital_clinic/list_view.html", context)

@login_required
def mcr_detail_view(request, pk):
    mcr = get_object_or_404(MCReport, pk = pk)
    
    context = {
        "app": "mc_reports",
        "obj": mcr,
        "additional_buttons": [
            {
                "url": "mc_reports:mcr-update",
                "bootstrap_class": "btn-outline-secondary",
                "bootstrap_icon": "bi-pencil",
                "text": "Edit",
            },{
                "url": "mc_reports:mcr-copy",
                "bootstrap_class": "btn-outline-secondary",
                "bootstrap_icon": "bi-copy",
                "text": "Copy",
            }, {
                "url": "mc_reports:mcr-print",
                "bootstrap_class": "btn-outline-secondary",
                "bootstrap_icon": "bi-printer",
                "text": "Print",
            }, {
                "url": "mc_reports:mcr-delete",
                "bootstrap_class": "btn-outline-danger",
                "bootstrap_icon": "bi-trash",
                "text": "Delete",
            }
        ],
        "url_list": "mc_reports:mcr-list"
    }
    
    return render(request, "mc_reports/mcr_detail.html", context)

class MCReportCreateView(LoginRequiredMixin, CreateView):
    model = MCReport
    form_class = MCReportForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app"] = "mc_reports"

        return context

class MCReportUpdateView(LoginRequiredMixin, UpdateView):
    model = MCReport
    form_class = MCReportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app"] = "mc_reports"

        return context

@login_required
def mcr_delete_view(request, pk):

    obj = get_object_or_404(MCReport, pk=pk)

    if request.method == "POST":
        obj.delete()
        return redirect("mc_reports:mcr-list")
    
    context = {
        "app": "mc_reports",
        "title": "MC Report",
        "obj": obj,
        "url_detail": "mc_reports:mcr-detail",
    }

    return render(request, "digital_clinic/delete_view.html", context)

@login_required
def mcr_print(request, pk):
    try:
        obj = (
            MCReport.objects
            .prefetch_related("patient")
            .get(pk=pk)
        )
    except MCReport.DoesNotExist:
        raise Http404("MC Report object not found")

    response = HttpResponse(generate_pdf(obj), content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=mcr.pdf"

    return response

@login_required
def mcr_copy(request, pk):
    obj = get_object_or_404(MCReport, pk=pk)

    fields = {
        field.name: getattr(obj, field.name)
        for field in obj._meta.fields
        if field != "id"
    }

    form = MCReportForm(fields)

    context = {
        "app": "mc_reports",
        "form": form
    }

    return render(request, "mc_reports/mcreport_form.html", context)


