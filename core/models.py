from django.db import models
from .fields import DayOfTheWeekField, DAY_OF_THE_WEEK


# Create your models here.
class StandardModel(models.Model):
    statut = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_upd = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DayOfTheWeek(models.Model):
    day = DayOfTheWeekField(unique=True)

    class Meta:
        verbose_name = "DayOfTheWeek"
        verbose_name_plural = "DayOfTheWeeks"

    def __str__(self):
        return str(self.day)

    @property
    def in_str(self):
        return DAY_OF_THE_WEEK[self.day]


class Contact(StandardModel):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    message = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.full_name} {self.message}"


class Newsletter(StandardModel):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    entreprise = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.full_name} {self.entreprise}"
