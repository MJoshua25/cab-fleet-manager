# vim: set fileencoding=utf-8 :
from django.contrib import admin

import core.models as models


class DayOfTheWeekAdmin(admin.ModelAdmin):

    list_display = ('id', 'day')
    list_filter = ('id', 'day')


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.DayOfTheWeek, DayOfTheWeekAdmin)
