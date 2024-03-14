# vim: set fileencoding=utf-8 :
from django.contrib import admin

import core.models as models


class DayOfTheWeekAdmin(admin.ModelAdmin):
    list_display = ('id', 'day')
    list_filter = ('id', 'day')


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'full_name',
        'email',
        'message'
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'full_name',
        'email',
        'message'
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.DayOfTheWeek, DayOfTheWeekAdmin)
