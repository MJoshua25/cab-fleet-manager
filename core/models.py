from django.db import models
from .fields import DayOfTheWeekField


# Create your models here.
class StandardModel(models.Model):
	statut = models.BooleanField(default=True)
	date_add = models.DateTimeField(auto_now_add=True)
	date_upd = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class DayOfTheWeek(models.Model):
	day = DayOfTheWeekField()

	class Meta:
		verbose_name = "DayOfTheWeek"
		verbose_name_plural = "DayOfTheWeeks"

	def __str__(self):
		return str(self.day)
