from django.contrib.auth.views import LoginView
from ..forms import CustomerAuthenticationForm

class CustomerLoginView(LoginView):
    authentication_form = CustomerAuthenticationForm
    template_name = 'sb/auth/login.html'
