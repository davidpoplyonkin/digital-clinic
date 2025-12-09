from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Model

class AutocompleteField(forms.Field):
    def __init__(self, model: Model, id_field: str, label: str, *args,
                 **kwargs):
        
        super().__init__(*args, **kwargs) 
        
        self.model = model

        # To which field in the model the user input corresponds (id, unique
        # name, etc.)
        self.id_field = id_field
        
        # How to refer to the object in the error message.
        self.label = label

    def to_python(self, value):
        # If value is empty, return None, allowing 'required' check to
        # fire later.

        if not value:
            return None

        try:
            # Check if such an objects exists.
            obj = self.model.objects.get(**{self.id_field: value})
        
        except self.model.DoesNotExist:
            raise ValidationError(
                f"No matching {self.label} found.",
                code='invalid_id'
            )

        return obj
    
    def prepare_value(self, value):
        value = super().prepare_value(value)

        if isinstance(value, int):
            # Get the string representation of the object.
            value = str(self.model.objects.get(pk=value))
        
        return value