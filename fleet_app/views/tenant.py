from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from fleet_app import models as fleet_models
from tenant.mixin import TenantAwareViewMixin
from tenant import models as tenant_models
from django.db import transaction
from django.utils import timezone
from fleet_app import forms as fleet_forms

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
	from tenant.models import Tenant


class CarListView(TenantAwareViewMixin, ListView):
	template_name = 'pages/tenant/fleet/car_list.html'
	form_class = fleet_forms.car.CreateCardForm

	def get_queryset(self):
		return fleet_models.Car.objects.filter(statut=True, tenant=self.tenant)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)

		if form.is_valid():
			car = fleet_models.Car(
				model=form.cleaned_data["model"],
				brand=form.cleaned_data["brand"],
				matriculation=form.cleaned_data["matriculation"],
				color=form.cleaned_data["color"],
				on_service=form.cleaned_data["on_service"],
				tenant=self.tenant
			)
			car.save()

		return self.get(request, *args, **kwargs)


class CarDetailView(TenantAwareViewMixin, DetailView):
	model = fleet_models.Car
	template_name = 'pages/tenant/fleet/car_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["now"] = timezone.now()
		return context


class CarUpdateView(TenantAwareViewMixin, DetailView):
	model = fleet_models.Car
	template_name = 'pages/tenant/fleet/car_modif.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["now"] = timezone.now()
		return context


def update_vehicule(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
	u_tenant: 'Tenant' = request.user.profile.tenant
	tenant = u_tenant

	if request.method != "POST":
		return redirect("core:tenant", tenant=tenant.unique_domain)

	# Getting datas from the form
	model = request.POST.get('model')
	brand = request.POST.get('brand')
	matriculation = request.POST.get('matriculation')
	color = request.POST.get('color')
	on_service = request.POST.get('on_service')

	# Updating the corresponding car object
	car = fleet_models.Car.objects.filter(statut=True, id=type_id)[:1].get()
	car.model = model
	car.brand = brand
	car.matriculation = matriculation
	car.color = color
	if on_service == 'on':
		car.on_service = True
	else:
		car.on_service = False

	car.save()

	return redirect('core:tenant:fleet:car_list', tenant=tenant.unique_domain)


def delete_vehicule(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
	tenant: 'Tenant' = request.user.profile.tenant
	tenant = tenant
	car = fleet_models.Car.objects.filter(statut=True, id=type_id)[:1].get()
	car.delete()
	return redirect('core:tenant:fleet:car_list', tenant=tenant.unique_domain)


class DriverListView(TenantAwareViewMixin, ListView):
	template_name = 'pages/tenant/fleet/driver_list.html'

	def get_queryset(self):
		return fleet_models.Driver.objects.filter(statut=True, tenant=self.tenant)


class ContractListView(TenantAwareViewMixin, ListView):
	template_name = 'pages/tenant/fleet/contract_list.html'

	def get_queryset(self):
		return fleet_models.Contract.objects.filter(statut=True, tenant=self.tenant)
