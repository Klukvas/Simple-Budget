from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from sb.models import SubCategory
from django import forms


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category', 'max_allowed_spend']  # Exclude 'user' as it will be set automatically
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subcategory Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'max_allowed_spend': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Allowed Spend'}),
        }
