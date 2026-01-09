from django import forms

from ..patients.models import Patient
from .models import MCReport
from ..core.forms.fields import AutocompleteField

class MCReportForm(forms.ModelForm):
    patient = AutocompleteField(Patient, "full_name", "patient")

    class Meta:
        model = MCReport
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs = {"type": "date"}),
        }
