from ..models.customer import Customer
from ..forms.signup import CustomerCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect

class CustomerSignUpView(CreateView):
    model = Customer
    form_class = CustomerCreationForm
    template_name = 'sb/auth/signup.html'
    success_url = reverse_lazy('sb:categories')

    def form_valid(self, form):
        user = form.save()
        raw_password = form.cleaned_data.get('password1')
        # Authenticate the user
        user = authenticate(username=user.email, password=raw_password)
        if user is not None:
            login(self.request, user)
        next_url = self.request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect('sb:categories')
