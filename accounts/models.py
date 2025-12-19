from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)


class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.shop_name


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username
