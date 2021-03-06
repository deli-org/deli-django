from django.db import models
from categories.models import Category
from accounts.models import Org

# Create your models here.


class Product(models.Model):
    name = models.TextField()
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UnitPrice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.IntegerField()
