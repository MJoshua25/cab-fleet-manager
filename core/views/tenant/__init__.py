from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from tenant.mixin import TenantAwareViewMixin

from fleet_app import models as fleet_app_models


class IndexView(TenantAwareViewMixin, TemplateView):
    template_name = 'pages/tenant/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars_number"] = fleet_app_models.Car.objects.filter(
            statut=True,
            tenant=self.tenant
        ).count()
        context["drivers_number"] = fleet_app_models.Driver.objects.filter(
            statut=True,
            tenant=self.tenant
        ).count()
        context["contract_number"] = fleet_app_models.Contract.objects.filter(
            statut=True,
            tenant=self.tenant
        ).count()
        context["payment_number"] = fleet_app_models.Expense.objects.filter(
            statut=True,
            tenant=self.tenant
        ).count()
        return context


class UserProfileView(TenantAwareViewMixin, TemplateView):
    template_name = 'pages/tenant/user_profil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars_number"] = fleet_app_models.Car.objects.filter(
            statut=True,
            tenant=self.tenant
        ).count()
        context["drivers_number"] = fleet_app_models.Driver.objects.filter(
            statut=True,
            tenant=self.tenant
        ).count()
        return context
