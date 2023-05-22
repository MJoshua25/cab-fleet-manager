from django.db import models
from tenant.models import TenantAwareModel
from django.contrib.auth.models import User


# Create your models here.

class FleetUser(TenantAwareModel):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

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

	class Meta:
		verbose_name = "Driver"
		verbose_name_plural = "Drivers"

	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.license_number})"
