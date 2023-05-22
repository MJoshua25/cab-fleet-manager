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
