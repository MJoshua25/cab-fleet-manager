# vim: set fileencoding=utf-8 :
from django.contrib import admin

import finance_app.models as models


class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'amount',
        'payment_method',
        'date_payment',
    )
    list_filter = (
        'statut',
        'date_add',
        'date_upd',
        'tenant',
        'date_payment',
        'id',
        'amount',
        'payment_method',
    )


class PaymentAdmin(admin.ModelAdmin):

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
        'contract',
        'date_payment',
        'is_sold_out',
        'id',
        'amount',
        'payment_method',
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Expense, ExpenseAdmin)
_register(models.Payment, PaymentAdmin)
