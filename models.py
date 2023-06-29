import functools
import math
from datetime import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.dispatch import receiver
import uuid as uuid
from functools import partial, reduce


# Create your models here.

class User(AbstractBaseUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    USERNAME_FIELD = 'username'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    #if user obj is created and saved in db
    if created:
        Token.objects.create(user=instance)


STATUS = [('parked', 'parked'), ('exited', 'exited')]


class Park(models.Model):
    name = models.CharField(max_length=100, unique=True)
    maximum_no_cars = models.IntegerField(default=20)
    charge_per_min = models.FloatField(default=0, null=False, blank=False)
    first_thirty_free = models.BooleanField(default=False, null=False, blank=False)
    lat = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    long = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    address = models.CharField(max_length=500)

    def number_of_parked_cars(self):
        return self.parkingtickets.filter(status=STATUS[0][1]).count()

    def has_space(self):
        """Check if currently parked cars are not more than
        maximum_no_cars
        """
        return self.available_space() > 0

    def available_space(self):
        """The number of space left."""
        parked_cars = self.parkingtickets.filter(status=STATUS[0][1])
        return self.maximum_no_cars - parked_cars.count()

    def is_parked(self, plate_number):
        parked = self.parkingtickets.filter(
            plate_number=plate_number, status=STATUS[0][1])
        return parked.exists()

    def __str__(self):
        return self.name


class ParkingTicket(models.Model):
    plate_number = models.CharField(max_length=10)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=STATUS, default="parked", max_length=7)
    park = models.ForeignKey(
        Park, related_name="parkingtickets", on_delete=models.CASCADE)
