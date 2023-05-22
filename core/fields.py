from django.db import models
from .utils import DAY_OF_THE_WEEK


class DaysChoice(models.IntegerChoices):
	for key, value in DAY_OF_THE_WEEK.items():
		locals()[value] = key


class DayOfTheWeekField(models.IntegerField):
	def __init__(self, *args, **kwargs):
		kwargs['choices'] = DaysChoice.choices
		super(DayOfTheWeekField, self).__init__(*args, **kwargs)
