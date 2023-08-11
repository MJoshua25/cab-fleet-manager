# vim: set fileencoding=utf-8 :
from django.contrib import admin

import fleet_app.models as models


class FleetUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'statut', 'date_add', 'date_upd', 'tenant', 'user', 'contact')
    list_filter = ('statut', 'date_add', 'date_upd', 'tenant', 'user', 'contact', 'id')


class CarAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'model',
        'brand',
        'matriculation',
        'color',
        'on_service'
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'on_service',
        'id',
        'model',
        'brand',
        'matriculation',
        'color'
    )


class DriverAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'last_name',
        'first_name',
        'phone_number',
        'license_number',
        'driver_license'
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'id',
        'last_name',
        'first_name',
        'phone_number',
        'license_number',
        'driver_license'
    )


class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'driver',
        'car',
        'is_active',
        'expect_daily_revenue',
        'holiday_expect_revenu'
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'driver',
        'car',
        'is_active',
        'id',
        'expect_daily_revenue',
        'holiday_expect_revenu'
    )
    raw_id_fields = ('rest_days',)


class InsuranceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'car',
        'insurance_company',
        'due_date',
        'monthly_amount',
        'last_payment',
        'next_date'
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'car',
        'due_date',
        'monthly_amount',
        'last_payment',
        'next_date'
    )


class InsurancePaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'amount',
        'contract',
        'payment_method',
        'date_payment',
        'is_sold_out',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'amount',
        'contract',
        'payment_method',
        'date_payment',
        'is_sold_out'
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.FleetUser, FleetUserAdmin)
_register(models.Car, CarAdmin)
_register(models.Driver, DriverAdmin)
_register(models.Contract, ContractAdmin)
_register(models.Insurance, InsuranceAdmin)
_register(models.InsurancePayment, InsurancePaymentAdmin)
