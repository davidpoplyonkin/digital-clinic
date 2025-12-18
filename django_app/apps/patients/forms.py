from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"
        widgets = {
            "dob": forms.DateInput(attrs = {"type": "date"}),
            "last_disp": forms.DateInput(attrs = {"type": "date"}),
            "last_colonoscopy": forms.DateInput(attrs = {"type": "date"}),
        }
