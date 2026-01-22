from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Patient
from .forms import PatientForm

@login_required
def patient_list_view(request):    
    context = {
        "app": "patients",
        "model": "Patient",
        "search_id": "search__full_name",
        "search_placeholder": "Patient Name",
        "url_create": "patients:patient-create",
    }

    return render(request, "digital_clinic/list_view.html", context)

@login_required
def patient_detail_view(request, pk):

    obj = get_object_or_404(Patient, pk = pk)

    obj_fields = []
    
    for field in obj._meta.fields:
        if field.name not in {"id", "full_name"}:
            obj_fields.append({
                "name": field.verbose_name.capitalize(),
                "value": getattr(obj, field.name)
            })      
    
    context = {
        "app": "patients",
        "obj": obj,
        "obj_fields": obj_fields,
        "buttons": {
            "back": "patients:patient-list",
            "edit": "patients:patient-update",
            "delete": "patients:patient-delete",
        }
    }
    
    return render(request, "patients/patient_detail.html", context)

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app"] = "patients"

        return context

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app"] = "patients"

        return context

@login_required
def patient_delete_view(request, pk):

    obj = get_object_or_404(Patient, pk = pk)

    if request.method == "POST":
        obj.delete()
        return redirect("patients:patient-list")
    
    context = {
        "app": "patients",
        "title": "Patient",
        "obj": obj,
        "url_detail": "patients:patient-detail",
    }

    return render(request, "digital_clinic/delete_view.html", context)
