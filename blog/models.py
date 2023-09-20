from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class AppUser(AbstractUser):
    pass


class Event(models.Model):
    class EventType(models.IntegerChoices):
        office = 1, "office"
        party = 2, "party"

    title = models.CharField(max_length=250)
    event_type = models.PositiveIntegerField(choices=EventType.choices)
    date = models.DateTimeField(null=True, blank=True)


class Employee(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    mail_status = models.BooleanField(default=False)
