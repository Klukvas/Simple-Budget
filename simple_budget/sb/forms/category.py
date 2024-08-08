from django import forms
from sb.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'max_allowed_spend']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'max_allowed_spend': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Allowed Spend'}),
        }
