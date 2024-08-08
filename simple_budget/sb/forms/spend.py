from sb.models import Spend
from django import forms


class SpendForm(forms.ModelForm):
    class Meta:
        model = Spend
        fields = ['category', 'subcategory', 'amount', 'date']  # Exclude 'user' as it will be set automatically
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Allowed Spend'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Spend date'})
            
        }
