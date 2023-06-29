from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.dispatch import receiver
import uuid as uuid


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


# class Customer(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=100)
#     car_model = models.CharField(max_length=100)
#     car_color = models.CharField(max_length=100)
#     comment = models.TextField(max_length=5000, blank=True)
#     cost_per_day = models.IntegerField(null=True, blank=True)
#     is_payed = models.BooleanField(default=False)
#     price = models.TextField(max_length=5000, blank=True)
#     device = models.TextField(max_length=5000, blank=True)
#     days_spent = models.CharField(null=True, blank=True, max_length=1000)
#     total_cost = models.IntegerField(null=True, blank=True)
#     register_name = models.CharField(max_length=100)
#     card_number = models.CharField(max_length=100)
#     reg_date = models.DateTimeField(auto_now_add=True)
#     exit_date = models.DateTimeField(null=True, blank=True)


# class Park(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     maximum_no_cars = models.IntegerField(default=10)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_modified = models.DateTimeField(auto_now=True)
#     charge_per_min = models.FloatField(default=0, null=False, blank=False)
#     first_thirty_free = models.BooleanField(default=False, null=False, blank=False)
#
#     def number_of_parked_cars(self):
#         return self.parkingtickets.filter(status=STATUS[0][1]).count()
#
#     def has_space(self):
#         """Check if currently parked cars are not more than
#         maximum_no_cars
#         """
#         return self.available_space() > 0
#
#     def available_space(self):
#         """The number of space left."""
#         parked_cars = self.parkingtickets.filter(status=STATUS[0][1])
#         return self.maximum_no_cars - parked_cars.count()
#
#     def get_days_specific_parkingtickets(self, days=None):
#         if not days:
#             return self.parkingtickets.all()
#         parked_time = timezone.now() - timedelta(days=int(days))
#         return self.parkingtickets.filter(entry_time__lte=parked_time)
#
#     def is_parked(self, plate_number):
#         parked = self.parkingtickets.filter(
#             plate_number=plate_number, status=STATUS[0][1])
#         return parked.exists()
#
#     def get_amount_paid(self, days=None):
#         sum_fee_paid = functools.partial(reduce_fee, z="fee_paid")
#         parkingtickets = self.get_days_specific_parkingtickets(days)
#         return functools.reduce(sum_fee_paid, parkingtickets, 0.0)
#
#     def get_amount_owned(self, days=None):
#         sum_amount_owned = functools.partial(reduce_fee, z="amount_owed")
#         parkingtickets = self.get_days_specific_parkingtickets(days)
#         return functools.reduce(sum_amount_owned, parkingtickets, 0.0)
#
#     def __str__(self):
#         return self.name
#
#
# class ParkingTicket(models.Model):
#     plate_number = models.CharField(max_length=9,
#                                     validators=[plate_number_validator])
#     entry_time = models.DateTimeField(auto_now_add=True)
#     exit_time = models.DateTimeField(blank=True, null=True)
#     checkout_time = models.DateTimeField(blank=True, null=True)
#     fee_paid = models.FloatField(default=0.0)
#     status = models.CharField(choices=STATUS, default="parked", max_length=7)
#     date_modified = models.DateTimeField(auto_now=True)
#     park = models.ForeignKey(
#         Park, related_name="parkingtickets", on_delete=models.CASCADE)
#     tenant = models.ForeignKey(
#         Tenant, related_name='tenant_parkingtickets', on_delete=models.CASCADE,
#         blank=True, null=True)
#
#     def get_ticket_fee(self):
#         THIRTY_MIN = 1800
#         stayed_time = timezone.now() - self.entry_time
#         stayed_time_seconds = stayed_time.total_seconds()
#
#         # left park within the first 30 minutes
#         if self.park.first_thirty_free and stayed_time_seconds <= THIRTY_MIN:
#             return 0.0
#         return math.ceil(stayed_time_seconds/60) * self.park.charge_per_min
#
#     def checkout(self):
#         if not self.checkout_time:
#             self.checkout_time = timezone.now()
#         return self.get_ticket_fee()
#
#     def amount_owed(self):
#         if self.tenant:
#             return 0.0
#         return self.get_ticket_fee() - self.fee_paid
#
#     def exit_park(self):
#         can_exit = self.amount_owed() <= 0
#         if can_exit:
#             self.status = 'exited'
#             self.exit_time = timezone.now()
#             self.save()
#         return can_exit
#
#     def pay_ticket(self, amount):
#         self.fee_paid += amount
#         self.save()
#
#     class Meta:
#         indexes = [
#             models.Index(fields=['plate_number']),
#             models.Index(fields=['park']),
#             models.Index(fields=['plate_number', 'park']),
#         ]
#
#
# class Vehicle(models.Model):
#     parkingnumber = models.CharField(max_length=20)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     vehiclecompany = models.CharField(max_length=50)
#     regno = models.CharField(max_length=10)
#     ownername = models.CharField(max_length=50)
#     ownercontact = models.CharField(max_length=15)
#     pdate = models.DateField()
#     intime = models.CharField(max_length=50)
#     outtime = models.CharField(max_length=50)
#     parkingcharge = models.CharField(max_length=50)
#     remark = models.CharField(max_length=500)
#     status = models.CharField(max_length=20)
#     def __str__(self):
#         return self.parkingnumber
#
