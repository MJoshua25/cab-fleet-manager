from django.db import models
from tenant.models import TenantAwareModel
from django.utils import timezone


# Create your models here.
class Expense(TenantAwareModel):
	amount = models.IntegerField(default=0)
	Payment_Method = models.CharField(max_length=100, null=True, blank=True)

	class Meta:
		verbose_name = "Expense"
		verbose_name_plural = "Expenses"

	def __str__(self):
		return f"{self.amount} {self.Payment_Method}"


class Payment(TenantAwareModel):
	amount = models.IntegerField(default=0)
	contract = models.ForeignKey('fleet_app.Contract', related_name="contract", on_delete=models.CASCADE)
	payment_method = models.CharField(max_length=100, blank=True, null=True)
	date_payment = models.DateField(default=timezone.now)
	is_sold_out = models.BooleanField(default=False)  # Je comprend pas trop ce champs

	class Meta:
		verbose_name = "Payment"
		verbose_name_plural = "Payments"

	def __str__(self):
		return f"{self.contract} {self.payment_method}"
