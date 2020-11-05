from django.db import models
from orgs.models import Org

# Create your models here.


class Product(models.Model):
    name = models.TextField()
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    price = models.IntegerField()


class UnitPrice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.IntegerField()
