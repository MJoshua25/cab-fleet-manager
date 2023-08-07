from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from fleet_app import models as fleet_models
from tenant.mixin import TenantAwareViewMixin
from tenant import models as tenant_models
from django.db import transaction
from django.utils import timezone

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from tenant.models import Tenant


class CarListView(TenantAwareViewMixin, ListView):
    template_name = 'pages/tenant/fleet/car_list.html'

    def get_queryset(self):
        return fleet_models.Car.objects.filter(statut=True, tenant=self.tenant)


class CarDetailView(TenantAwareViewMixin, DetailView):
    model = fleet_models.Car
    template_name = 'pages/tenant/fleet/car_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


def add_vehicule(request: HttpRequest, tenant: str) -> HttpResponse:
    tenant: 'Tenant' = request.user.profile.tenant
    if request.method == "POST":
        model = request.POST.get('model')
        brand = request.POST.get('brand')
        matriculation = request.POST.get('matriculation')
        color = request.POST.get('color')
        on_service = request.POST.get('on_service')
        if on_service == 'on':
            on_service = True
        else:
            on_service = False
        car = fleet_models.Car(
            model=model,
            brand=brand,
            matriculation=matriculation,
            color=color,
            on_service=True if on_service == 'on' else on_service != 'on',
            tenant=tenant
        )
        car.save()

        return redirect('core:tenant:fleet:car_list', tenant=tenant.unique_domain)
    else:
        return redirect("core:tenant", tenant=tenant.unique_domain)


class CarUpdateView(TenantAwareViewMixin, DetailView):
    model = fleet_models.Car
    template_name = 'pages/tenant/fleet/car_modif.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


def update_vehicule(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
    tenant: 'Tenant' = request.user.profile.tenant
    if request.method == "POST":
        model = request.POST.get('model')
        brand = request.POST.get('brand')
        matriculation = request.POST.get('matriculation')
        color = request.POST.get('color')
        on_service = request.POST.get('on_service')
        car = fleet_models.Car.objects.filter(statut=True, id=type_id)[:1].get()
        car.model = model,
        car.brand = brand,
        car.matriculation = matriculation,
        car.color = color,
        if on_service == 'on':
            car.on_service = True
        else:
            car.on_service = False
        print(car.on_service)
        tenant = tenant
        car.save()

        return redirect('core:tenant:fleet:car_list', tenant=tenant.unique_domain)
    else:
        return redirect("core:tenant", tenant=tenant.unique_domain)


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
