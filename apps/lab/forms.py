from django import forms

from ..patients.models import Patient
from .models import Lab, TestResult
from ..core.forms.fields import AutocompleteField

class LabWizardLabForm(forms.ModelForm):
    patient = AutocompleteField(Patient, "full_name", "patient")
    date = forms.DateField(widget = forms.DateInput(attrs = {"type": "date"}))
    place = forms.CharField()

    class Meta:
        model = Lab
        fields = ["patient", "date", "place"]

class LabWizardResForm(forms.ModelForm):
    # NOTE: On the one hand, combining panel and test results in one step
    # entails extra work with the wizard, given that it doesn't natively
    # support multiple forms in one step. On the other hand, this really
    # simplifies prefilling of the formset: it is only necessary to retrieve
    # the results associated with the current panel, whereas adding new forms
    # or deleting the old ones in response to changes in the panel name can be
    # delegated to HTMX.

    class Meta:
        model = Lab
        fields = ["panel"]

class LabWizardResFormSetForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ["value", "cs", "test", "order"]

LabWizardResFormSet = forms.inlineformset_factory(
    Lab,
    TestResult,
    form=LabWizardResFormSetForm,
    can_delete=True,
    extra=0,
)

class LabWizardResStep(forms.Form):
    """
    A dummy class to represent the combined LabForm and LabTestResFormSet
    step in the form wizard.
    """

    def __init__(self, form: forms.ModelForm, formset: forms.BaseInlineFormSet,
                 *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.form = form
        self.formset = formset

    def is_valid(self):
        # Check if the provided panel name is valid.
        if self.form.is_valid():
            # If so, pass the instance to the formset, and validate it.
            lab = self.form.save(commit=False)
            self.formset.instance = lab
            if self.formset.is_valid():
                return True
            
        return False

    def save(self):
        lab = self.form.save()
        self.formset.instance = lab
        self.formset.save()

        return lab
