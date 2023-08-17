from django.db import models

from core.fields import DayOfTheWeekField
from tenant.models import TenantAwareModel, StandardModel
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from finance_app.models import Expense
from django.utils import timezone


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
    name_slug = AutoSlugField(populate_from='model', unique_with=['id', 'date_add'])
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
        return f"{self.brand} {self.matriculation}"


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

    @property
    def name(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Contract(TenantAwareModel):
    driver = models.ForeignKey(Driver, related_name="contratChauffeur", on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name="contratVoiture", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    expect_daily_revenue = models.IntegerField(default=0)
    holiday_expect_revenu = models.IntegerField(default=0)
    rest_days = models.ManyToManyField('core.DayOfTheWeek', related_name='jours')

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return str(self.driver)


class OutageReason(StandardModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = "OutageReason"
        verbose_name_plural = "OutageReasons"

    def __str__(self):
        return str(self.name)


class Insurance(TenantAwareModel):
    car = models.ForeignKey(Car, related_name="voitureAssurance", on_delete=models.CASCADE)
    insurance_company = models.CharField(max_length=100)
    due_date = models.DateTimeField(auto_now=True)
    monthly_amount = models.IntegerField()
    last_payment = models.IntegerField(default=0)
    next_date = models.DateTimeField()

    class Meta:
        verbose_name = "Insurance"
        verbose_name_plural = "Insurances"

    def __str__(self):
        return f"{self.car} {self.insurance_company}"


class InsurancePayment(Expense):
    insurance = models.ForeignKey(Insurance, related_name='payments', on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, related_name="InsurancePayment", on_delete=models.CASCADE)
    is_sold_out = models.BooleanField(default=False)  # Je comprend pas trop ce champs

    class Meta:
        verbose_name = "InsurancePayment"
        verbose_name_plural = "InsurancePayments"

    def __str__(self):
        return f"{self.contract} {self.payment_method}"


class Outage(Expense):
    car = models.ForeignKey(Car, related_name="outages", on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, related_name="outages", on_delete=models.CASCADE)
    reason = models.ForeignKey(OutageReason, related_name="outages", on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    is_okay = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Outage"
        verbose_name_plural = "Outages"


class OilChange(Expense):
    car = models.ForeignKey(Car, related_name="voitureVidange", on_delete=models.CASCADE)
    oil_type = models.CharField(max_length=100)
    service_center = models.CharField(max_length=100)
    date_OilChange = models.DateTimeField(auto_now_add=True)
    date_next_oil_change = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "OilChange"
        verbose_name_plural = "OilChanges"
