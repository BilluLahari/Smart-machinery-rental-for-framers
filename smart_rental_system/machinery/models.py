from django.contrib.auth.models import User
from django.db import models


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_hour = models.DecimalField(max_digits=10,decimal_places=2)
    price_per_week = models.DecimalField(max_digits=10,decimal_places=2)
    price_per_15_days = models.DecimalField(max_digits=10,decimal_places=2)
    price_per_month = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='equipment_images/', blank=True, null=True)
    renter_name = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name



class RentalRequest(models.Model):
    machinery = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    renter = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.renter.username} - {self.machinery.name}"
