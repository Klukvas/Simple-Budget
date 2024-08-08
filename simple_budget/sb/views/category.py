from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin


from django.db.models import Sum


from sb.forms import CategoryForm

from sb.models import Category

class CategoryListView(LoginRequiredMixin, ListView):

    login_url = "/simple-budget/login/"

    model = Category
    paginate_by = 100
    template_name = 'sb/category/list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.prefetch_related('sub_categories').filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()  # Call get_queryset only once

        context['total_categories_count'] = queryset.count()

        total_max_allowed = queryset.aggregate(total_max_allowed=Sum('max_allowed_spend'))
        context['total_max_allowed'] = total_max_allowed['total_max_allowed'] or 0

        return context

class CategoryCreateView(LoginRequiredMixin, CreateView):
    login_url = "/simple-budget/login/"

    model = Category
    form_class = CategoryForm
    template_name = 'sb/category/create.html'
    success_url = reverse_lazy('sb:categories')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/simple-budget/login/"

    model = Category
    success_url = reverse_lazy('sb:categories')
    template_name = 'sb/category_confirm_delete.html'

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/simple-budget/login/"

    model = Category
    form_class = CategoryForm
    template_name = 'sb/category/detail.html'
    success_url = reverse_lazy('sb:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        print(category)
        context['subcategories'] = category.sub_categories.all()
        return context
