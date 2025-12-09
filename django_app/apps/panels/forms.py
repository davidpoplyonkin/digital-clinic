from django import forms

from .models import (Panel, PanelTest)

class PanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ["name"]

class PanelTestForm(forms.ModelForm):
    class Meta:
        model = PanelTest
        fields = ["test", "order"]

PanelTestFormSet = forms.inlineformset_factory(
    Panel,
    PanelTest,
    form=PanelTestForm,
    extra=0,
    can_delete=True,
)