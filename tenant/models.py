from django.db import models
from core.models import StandardModel
from django.utils.text import slugify


# Create your models here.

class Tenant(StandardModel):
	name = models.CharField(max_length=100)
	unique_domain = models.CharField(unique=True, max_length=255)

	class Meta:
		verbose_name = "Tenant"
		verbose_name_plural = "Tenants"

	def __str__(self) -> 'str':
		return f'{self.unique_domain}'


class TenantAwareModel(StandardModel):
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

	class Meta:
		abstract = True
