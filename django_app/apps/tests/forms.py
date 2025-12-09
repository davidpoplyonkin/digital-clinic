from django import forms
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Test, TestAgeGroup

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = "__all__"

class TestAgeGroupForm(forms.ModelForm):
    class Meta:
        model = TestAgeGroup
        fields = "__all__"

    def clean(self):
            cleaned_data = super().clean()

            # Make sure that max is greater than min.
            male_min = cleaned_data.get("male_min")
            male_max = cleaned_data.get("male_max")
            female_min = cleaned_data.get("female_min")
            female_max = cleaned_data.get("female_max")         

            if (male_min is not None) and (male_max is not None) :
                if male_max < male_min:
                    msg = "Max value cannot be less the min value."
                    self.add_error("male_max", ValidationError(msg))

            if (female_min is not None) and (female_max is not None):
                if female_max < female_min:
                    msg = "Max value cannot be less the min value."
                    self.add_error("female_max", ValidationError(msg))

            return cleaned_data
    
class TestAgeGroupFormSetTemplate(BaseInlineFormSet):
    # It is needed to add custom validation.

    def clean(self):
        super().clean()

        # Do nothing unless each form is valid.
        if any(self.errors):
            return

        prev_max_age = 0

        for f in self.forms:
            form_data = f.cleaned_data

            # Skip the forms marked for deletion and the empty forms.
            # The latter aren't caught by `if any(self.errors)`.
            if form_data.get("DELETE") or (form_data.get("max_age") is None):
                continue
            
            if (form_data.get("max_age") > prev_max_age):
                # It is safe to compare like above since the forms are
                # guaranteed to be valid.

                prev_max_age = form_data.get("max_age")

            else:
                msg = "Max ages must be in ascending order."
                f.add_error("max_age", ValidationError(msg))

TestAgeGroupFormSet = forms.inlineformset_factory(
    Test,
    TestAgeGroup,
    form = TestAgeGroupForm,
    formset = TestAgeGroupFormSetTemplate,
    extra = 0,
    can_delete = True,
)
