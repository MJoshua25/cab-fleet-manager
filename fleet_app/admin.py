# vim: set fileencoding=utf-8 :
from django.contrib import admin

import fleet_app.models as models


class FleetUserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'user',
        'contact',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'user',
        'id',
        'contact',
    )


class CarAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'name_slug',
        'model',
        'brand',
        'matriculation',
        'color',
        'on_service',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'on_service',
        'id',
        'name_slug',
        'model',
        'brand',
        'matriculation',
        'color',
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
        'driver_license',
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
        'driver_license',
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
        'holiday_expect_revenu',
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
        'holiday_expect_revenu',
    )
    raw_id_fields = ('rest_days',)


class OutageReasonAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'name',
        'description',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'id',
        'name',
        'description',
    )
    search_fields = ('name',)


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
        'next_date',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'car',
        'due_date',
        'next_date',
        'id',
        'insurance_company',
        'monthly_amount',
        'last_payment',
    )


class InsurancePaymentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'amount',
        'payment_method',
        'date_payment',
        'insurance',
        'contract',
        'is_sold_out',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'date_payment',
        'insurance',
        'contract',
        'is_sold_out',
        'id',
        'amount',
        'payment_method',
    )


class OutageAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'amount',
        'payment_method',
        'date_payment',
        'car',
        'driver',
        'reason',
        'location',
        'is_okay',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'date_payment',
        'car',
        'driver',
        'reason',
        'is_okay',
        'id',
        'amount',
        'payment_method',
        'location',
    )


class OilChangeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'amount',
        'payment_method',
        'date_payment',
        'car',
        'oil_type',
        'service_center',
        'date_OilChange',
        'date_next_oil_change',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'date_payment',
        'car',
        'date_OilChange',
        'date_next_oil_change',
        'id',
        'amount',
        'payment_method',
        'oil_type',
        'service_center',
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.FleetUser, FleetUserAdmin)
_register(models.Car, CarAdmin)
_register(models.Driver, DriverAdmin)
_register(models.Contract, ContractAdmin)
_register(models.OutageReason, OutageReasonAdmin)
_register(models.Insurance, InsuranceAdmin)
_register(models.InsurancePayment, InsurancePaymentAdmin)
_register(models.Outage, OutageAdmin)
_register(models.OilChange, OilChangeAdmin)
