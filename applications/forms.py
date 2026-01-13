from django import forms
from .models import ApplicationType, ApplicationField


class DynamicApplicationForm(forms.Form):
    """Dynamically generated form based on ApplicationField"""
    
    def __init__(self, application_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get all fields for this application type
        fields = ApplicationField.objects.filter(
            application_type=application_type,
            application_type__is_active=True
        ).order_by('order')
        
        # Dynamically add form fields
        for field in fields:
            field_kwargs = {
                'label': field.label,
                'required': field.is_required,
                'help_text': field.help_text,
            }
            
            if field.placeholder:
                field_kwargs['widget'] = forms.TextInput(attrs={'placeholder': field.placeholder})
            
            if field.field_type == 'textarea':
                field_kwargs['widget'] = forms.Textarea(attrs={
                    'placeholder': field.placeholder,
                    'rows': 4,
                    'class': 'form-control'
                })
            elif field.field_type == 'email':
                field_kwargs['widget'] = forms.EmailInput(attrs={'placeholder': field.placeholder})
            elif field.field_type == 'date':
                field_kwargs['widget'] = forms.DateInput(attrs={'type': 'date', 'placeholder': field.placeholder})
            elif field.field_type == 'number':
                field_kwargs['widget'] = forms.NumberInput(attrs={'placeholder': field.placeholder})
            elif field.field_type == 'select':
                options = [opt.strip() for opt in field.options.split(',') if opt.strip()]
                field_kwargs['widget'] = forms.Select(choices=[(opt, opt) for opt in options])
            elif field.field_type == 'checkbox':
                field_kwargs['widget'] = forms.CheckboxInput()
            
            if field.validation_regex:
                field_kwargs['widget'].attrs['pattern'] = field.validation_regex
            
            self.fields[field.field_name] = self._get_field_class(field.field_type)(**field_kwargs)
    
    def _get_field_class(self, field_type):
        """Return appropriate form field class"""
        field_map = {
            'text': forms.CharField,
            'textarea': forms.CharField,
            'email': forms.EmailField,
            'date': forms.DateField,
            'number': forms.IntegerField,
            'select': forms.ChoiceField,
            'checkbox': forms.BooleanField,
        }
        return field_map.get(field_type, forms.CharField)


