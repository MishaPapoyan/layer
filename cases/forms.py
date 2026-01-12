from django import forms
from .models import CaseAnalysis


class CaseAnalysisForm(forms.ModelForm):
    class Meta:
        model = CaseAnalysis
        fields = ['hypothesis', 'legal_qualification', 'conclusion']
        widgets = {
            'hypothesis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter your investigative hypothesis...',
                'style': 'min-height: 140px; padding: 1rem 1.25rem;'
            }),
            'legal_qualification': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter legal qualification...',
                'style': 'min-height: 140px; padding: 1rem 1.25rem;'
            }),
            'conclusion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter your legal conclusion...',
                'style': 'min-height: 140px; padding: 1rem 1.25rem;'
            }),
        }

