from django.db import models
from accounts.models import Org
from products.models import Product, UnitPrice
# Create your models here.


class SaleManager(models.Manager):
    def open(self):
        return self.filter(paid=False)


class Sale(models.Model):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'
    CASH = 'CASH'

    PAYMENT_CHOICES = [
        (DEBIT, 'debit'),
        (CREDIT, 'credit'),
        (CASH, 'cash')
    ]

    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    identifier = models.CharField(max_length=100, unique=True)
    payment_type = models.CharField(
        max_length=6, choices=PAYMENT_CHOICES, null=True)


class SaleDetail(models.Model):
    sale = models.ForeignKey(
        Sale, related_name='saledetails', on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField()
    discount = models.IntegerField(default=0)
    unitprice = models.ForeignKey(UnitPrice, on_delete=models.CASCADE)
