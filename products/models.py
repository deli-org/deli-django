from django.db import models
from categories.models import Category
from accounts.models import Org

# Create your models here.


class Product(models.Model):
    name = models.TextField()
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    price = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)


class UnitPrice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.IntegerField()
