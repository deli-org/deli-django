from django.db import models
from accounts.models import Org


class Category(models.Model):
    name = models.TextField()
    org = models.ForeignKey(Org, on_delete=models.CASCADE)

    def __str__(self):
        return f'id: {self.id}, name: {self.name}'

    class Meta:
        verbose_name_plural = "Categories"

# Create your models here.
