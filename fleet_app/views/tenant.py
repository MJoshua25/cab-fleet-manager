from django.views.generic import ListView
from fleet_app import models as fleet_models
from tenant.mixin import TenantAwareViewMixin


class CarListView(TenantAwareViewMixin, ListView):
	template_name = 'pages/tenant/fleet/car_list.html'

	def get_queryset(self):
		return fleet_models.Car.objects.filter(statut=True, tenant=self.tenant)


class DriverListView(TenantAwareViewMixin, ListView):
	template_name = 'pages/tenant/fleet/driver_list.html'

	def get_queryset(self):
		return fleet_models.Driver.objects.filter(statut=True, tenant=self.tenant)


class ContractListView(TenantAwareViewMixin, ListView):
	template_name = 'pages/tenant/fleet/contract_list.html'

	def get_queryset(self):
		return fleet_models.Contract.objects.filter(statut=True, tenant=self.tenant)
