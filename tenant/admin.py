# vim: set fileencoding=utf-8 :
from django.contrib import admin

import tenant.models as models


class TenantAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'name',
        'unique_domain',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'id',
        'name',
        'unique_domain',
    )
    search_fields = ('name',)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Tenant, TenantAdmin)
