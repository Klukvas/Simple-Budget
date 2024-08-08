from django.db import models
from django.urls import reverse
from .customer import Customer


class Category(models.Model):
    name = models.CharField()
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='Categories')
    max_allowed_spend = models.IntegerField(null=True, blank = True)

    def __str__(self) -> str:
        return self.name
