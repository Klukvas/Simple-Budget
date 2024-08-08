from django.db import models
from .category import Category
from .subcategory import SubCategory
from .customer import Customer

from django.utils import timezone

from django.db.models import Sum, F, Q
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils import timezone
from django.db.models import Sum, F, Q
from django.db.models.functions import ExtractMonth, ExtractYear

class SpendQuerySet(models.QuerySet):

    def get_current_and_previous_months(self):
        now = timezone.now()
        current_month = now.month
        current_year = now.year

        if current_month == 1:
            prev_month = 12
            prev_year = current_year - 1
        else:
            prev_month = current_month - 1
            prev_year = current_year
        
        return {
            "current_month": current_month,
            "current_year": current_year,
            "prev_month": prev_month,
            "prev_year": prev_year
        }

    def current_month_spends(self):
        months = self.get_current_and_previous_months()
        return self.annotate(month=ExtractMonth('date'), year=ExtractYear('date')) \
                   .filter(month=months['current_month'], year=months['current_year'])

    def spends_for_current_month_by_category(self):
        return self.current_month_spends() \
                   .select_related('category') \
                   .values(category_name=F('category__name')) \
                   .annotate(total_amount=Sum('amount')) \
                   .order_by('category_name')

    def spends_for_current_and_previous_months_by_category(self):
        months = self.get_current_and_previous_months()
        return self.select_related('category') \
                   .annotate(month=ExtractMonth('date'), year=ExtractYear('date')) \
                   .filter(
                       Q(month=months['current_month'], year=months['current_year']) | 
                       Q(month=months['prev_month'], year=months['prev_year'])
                   ) \
                   .values(category_name=F('category__name'), month=F('month'), year=F('year')) \
                   .annotate(total_amount=Sum('amount')) \
                   .order_by('category_name', 'year', 'month')
    
    def current_month_spends_with_max_allowed_by_category(self):
        return self.current_month_spends() \
            .values(max_spend=F('category__max_allowed_spend'), category_name=F('category__name')) \
            .filter(max_spend__isnull=False) \
            .annotate(current_spend=Sum('amount')) \
            .order_by('category_name')

class Spend(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='spends')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING, related_name='spends', null=True, blank=True)
    amount = models.FloatField()
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='spends')

    objects = SpendQuerySet.as_manager()
