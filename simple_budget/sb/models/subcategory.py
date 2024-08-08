from django.db import models
from .category import Category
from django.urls import reverse
from .customer import Customer


class SubCategory(models.Model):
    name = models.CharField()
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sub_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')
    max_allowed_spend = models.IntegerField(null=True, blank = True)

    def __str__(self) -> str:
        return self.name
