from django.views.generic.edit import UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from sb.forms import CustomerForm

from sb.models import Customer


class AccountUpdateView(LoginRequiredMixin, UpdateView):

    login_url = "/simple-budget/login/"
    # redirect_field_name = "redirect_to"

    model = Customer
    form_class = CustomerForm
    template_name = 'sb/account/info.html'
    success_url = reverse_lazy('account_info')

    def get_object(self, queryset=None):
        return self.request.user
