from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from sb.forms import SpendForm
from sb.models import Spend


class SpendListView(LoginRequiredMixin, ListView):
    login_url = "/simple-budget/login/"

    model = Spend
    paginate_by = 100
    template_name = 'sb/spend/list.html'

    context_object_name = 'spends'

    def get_queryset(self):
        return Spend.objects.filter(user=self.request.user).order_by('-date')

class SpendCreateView(LoginRequiredMixin, CreateView):
    login_url = "/simple-budget/login/"

    model = Spend
    form_class = SpendForm
    template_name = 'sb/spend/create.html'
    success_url = reverse_lazy('sb:spends')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)