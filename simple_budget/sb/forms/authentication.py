from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class CustomerAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class': 'form-control', 'autofocus': True}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = None  # No model is associated with AuthenticationForm
        fields = ['username', 'password']
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control', 'autofocus': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
