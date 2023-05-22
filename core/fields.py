from django.db import models
from .utils import DAY_OF_THE_WEEK


class DaysChoice(models.IntegerChoices):
	global key, value, variable_name
	for key, value in DAY_OF_THE_WEEK.items():
		variable_name = value.replace(" ", "").replace("-", "").replace("'", "")
		locals()[variable_name] = key


class DayOfTheWeekField(models.IntegerField):
	def __init__(self, *args, **kwargs):
		kwargs['choices'] = DaysChoice.choices
		super(DayOfTheWeekField, self).__init__(*args, **kwargs)
