from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class AppUser(AbstractUser):
    pass


class Blog(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField(max_length=250)
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE)
