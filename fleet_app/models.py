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
    driver_license = models.FileField(upload_to='uploads/')

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


class Expenses(models.Model):
    amount = models.IntegerField(max_length=100)
    Payment_Method = models.CharField(max_length=100)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"{self.amount} {self.Payment_Method}"


class Outages(Expenses):
    car = models.ForeignKey(Car, related_name="contract", on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, related_name="contract", on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=100)
    is_Okay = models.BooleanField()

    class Meta:
        verbose_name = "Outage"
        verbose_name_plural = "Outages"


class Insurance(Expenses):
    car = models.ForeignKey(Car, related_name="contract", on_delete=models.CASCADE)
    insurance_company = models.CharField(max_length=100)
    validity_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Insurance"
        verbose_name_plural = "Insurances"


class OilChange(Expenses):
    car = models.ForeignKey(Car, related_name="contract", on_delete=models.CASCADE)
    OilType = models.CharField(max_length=100)
    service_center = models.CharField(max_length=100)

    class Meta:
        verbose_name = "OilChange"
        verbose_name_plural = "OilChanges"
