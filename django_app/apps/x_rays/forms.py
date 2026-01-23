from django import forms

from ..patients.models import Patient
from .models import XRaysExamination
from ..core.forms.fields import AutocompleteField

class XRaysForm(forms.ModelForm):
    patient = AutocompleteField(Patient, "full_name", "patient")

    class Meta:
        model = XRaysExamination
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs = {"type": "date"}),
        }