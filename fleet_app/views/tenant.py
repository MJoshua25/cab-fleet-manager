from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from fleet_app import models as fleet_models
from tenant.mixin import TenantAwareViewMixin
from tenant import models as tenant_models
from django.db import transaction
from django.utils import timezone


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


def add_vehicule(request: HttpRequest) -> HttpResponse:
    tenant = request.user.profile.tenant
    if request.method == "POST":
        model = request.POST.get('model')
        brand = request.POST.get('brand')
        matriculation = request.POST.get('matriculation')
        color = request.POST.get('color')
        act_tenant = tenant_models.Tenant(
            name=request.tenant.name,
            unique_domain=request.tenant.unique_domain
        )
        create = fleet_models.Car(
            model=model,
            brand=brand,
            matriculation=matriculation,
            color=color,
            on_service=True
        )
        with transaction.atomic():
            act_tenant.save()
            create.save()

        return redirect('core:tenant:fleet:car_list', tenant=tenant.unique_domain)
    else:
        return redirect("core:tenant", tenant=tenant.unique_domain)


class DriverListView(TenantAwareViewMixin, ListView):
    template_name = 'pages/tenant/fleet/driver_list.html'

    def get_queryset(self):
        return fleet_models.Driver.objects.filter(statut=True, tenant=self.tenant)


class ContractListView(TenantAwareViewMixin, ListView):
    template_name = 'pages/tenant/fleet/contract_list.html'

    def get_queryset(self):
        return fleet_models.Contract.objects.filter(statut=True, tenant=self.tenant)
