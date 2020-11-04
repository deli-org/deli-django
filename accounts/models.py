from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Org(models.Model):
    name = models.CharField(max_length=100)


class User(AbstractUser):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
