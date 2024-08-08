from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from sb.forms import SubCategoryForm
from sb.models import SubCategory, Category
from django.http import JsonResponse
from django.db.models import Sum
from sb.models.subcategory import SubCategory


class SubcategoryListView(LoginRequiredMixin, ListView):
    login_url = "/simple-budget/login/"

    model = SubCategory
    paginate_by = 100
    template_name = 'sb/subcategory/list.html'
    context_object_name = 'subcategories'

    def get_queryset(self):
        return SubCategory.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        context['total_categories_count'] = queryset.count()

        total_max_allowed = queryset.aggregate(total_max_allowed=Sum('max_allowed_spend'))
        context['total_max_allowed'] = total_max_allowed['total_max_allowed'] or 0

        return context

class SubCategoryCreateView(LoginRequiredMixin, CreateView):
    login_url = "/simple-budget/login/"

    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'sb/subcategory/create.html'
    success_url = reverse_lazy('sb:subcategories')

    def form_valid(self, form):
        # Retrieve the category and user from the form
        category = form.cleaned_data['category']
        user = self.request.user

        # Ensure the category belongs to the current user
        category = Category.objects.filter(name=category, user=user).first()
        if not category:
            form.add_error('category', 'Category not found or does not belong to you.')
            return self.form_invalid(form)

        # Calculate the total amount of all subcategories for the category by this user
        total_existing_amount = SubCategory.objects.filter(
            category=category, user=user
        ).aggregate(total_amount=Sum('max_allowed_spend'))['total_amount'] or 0

        # Add the amount from the form
        new_amount = form.cleaned_data['max_allowed_spend']
        total_with_new_amount = total_existing_amount + new_amount

        # Check if this exceeds the category's max_allowed_spend
        if total_with_new_amount > category.max_allowed_spend:
            form.add_error(
                'max_allowed_spend',
                ValidationError(
                    f'The total amount of subcategories for this category ({total_with_new_amount}) exceeds the allowed limit of {category.max_allowed_spend}.'
                )
            )
            return self.form_invalid(form)

        # Set the user of the subcategory instance
        form.instance.user = user

        return super().form_valid(form)

class GetSubcategoriesView(LoginRequiredMixin, View):
    login_url = "/simple-budget/login/"

    def get(self, request, category_id):
        user = request.user
        subcategories = SubCategory.objects.filter(category_id=category_id, user=user)
        data = {'subcategories': list(subcategories.values('id', 'name'))}
        return JsonResponse(data)


class SubCategoryUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/simple-budget/login/"

    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'sb/subcategory/detail.html'
    context_object_name = 'subcategory'
    success_url = reverse_lazy('sb:subcategories')


class SubcategoryDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/simple-budget/login/"

    model = SubCategory
    success_url = reverse_lazy('sb:subcategories')