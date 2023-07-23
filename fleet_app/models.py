from django.db import models
from tenant.models import TenantAwareModel
from django.contrib.auth.models import User


# Create your models here.

class FleetUser(TenantAwareModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    contact = models.CharField(max_length=10)

    class Meta:
        verbose_name = "FleetUser"
        verbose_name_plural = "FleetUsers"

    def __str__(self):
        return self.user.username


class Car(TenantAwareModel):
    model = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    matriculation = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    on_service = models.BooleanField(default=True)
    VehiculePaper = models.FileField(upload_to='uploads/')

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"
        unique_together = ("tenant", "matriculation")

    def __str__(self):
        return self.matriculation


class Driver(TenantAwareModel):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.license_number})"


class Contract(TenantAwareModel):
    driver = models.ForeignKey(Driver, related_name="contract", on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name="contract", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    expect_daily_revenue = models.IntegerField(default=0)
    holiday_expect_revenu = models.IntegerField(default=0)
    rest_days = models.ManyToManyField('core.DayOfTheWeek', related_name='contracts')

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return str(self.driver)
