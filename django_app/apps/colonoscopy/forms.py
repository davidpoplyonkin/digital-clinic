from django import forms

from .models import ColonoscopyReport, PhotoProtocolImage
from ..patients.models import Patient
from ..core.forms.fields import AutocompleteField


class PassportForm(forms.ModelForm):
    patient = AutocompleteField(Patient, "full_name", "patient")
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"}), required=False,
    )

    class Meta:
        model = ColonoscopyReport
        fields = [
            "patient",
            "organization",
            "colonoscopist",
            "colonoscopist_phone",
            "procedure",
            "date",
            "time",
            "doctor",
            "doctor_phone",
        ]

class EvidenceForm(forms.ModelForm):
    class Meta:
        model = ColonoscopyReport
        fields = [
            "diagnosis",
            "evidence",
            "asa_classification",
            "sedation",
            "anesthetist",
        ]

class ResultsForm(forms.ModelForm):
    class Meta:
        model = ColonoscopyReport
        fields = [
            "bowel_prep",
            "bbps",
            "insertion_level",
            "visualization",
            "biopsy_referral",
            "withdrawal_time"
        ]

class PhotoProtocolImageForm(forms.ModelForm):
    class Meta:
        model = PhotoProtocolImage
        fields = "__all__"

PhotoProtocolFormSet = forms.inlineformset_factory(
    ColonoscopyReport,
    PhotoProtocolImage,
    form=PhotoProtocolImageForm,
    can_delete=True,
    extra=0,
)

class InterventionsForm(forms.ModelForm):
    class Meta:
        model = ColonoscopyReport
        fields = [
            "finger_examination",
            "ileum",
            "right_colon",
            "colon_transversum",
            "colon_descendens",
            "sigmoid",
            "rectum",
        ]

class AdverseEventsForm(forms.ModelForm):
    class Meta:
        model = ColonoscopyReport
        fields = [
            "adverse_events",
        ]

class ConclusionForm(forms.ModelForm):
    class Meta:
        model = ColonoscopyReport
        fields = [
            "conclusion",
        ]

class RecommendationsForm(forms.ModelForm):
    class Meta:
        model = ColonoscopyReport
        fields = [
            "next_colonoscopy",
            "follow_up_with",
            "recommendations",
        ]
