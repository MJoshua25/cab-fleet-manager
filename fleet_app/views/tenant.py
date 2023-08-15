from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from fleet_app import models as fleet_models
from core import models as core_models
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


class DriverDetailView(TenantAwareViewMixin, DetailView):
    model = fleet_models.Driver
    template_name = 'pages/tenant/fleet/driver_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


def add_driver(request: HttpRequest, tenant: str) -> HttpResponse:
    tenant: 'Tenant' = request.user.profile.tenant
    if request.method == "POST":
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        phone_number = request.POST.get('phone_number')
        license_number = request.POST.get('license_number')
        driver_license = request.FILES.get('driver_license')
        print(driver_license)
        driver = fleet_models.Driver(
            last_name=last_name,
            first_name=first_name,
            phone_number=phone_number,
            license_number=license_number,
            driver_license=driver_license,
            tenant=tenant
        )
        driver.save()

        return redirect('core:tenant:fleet:driver_list', tenant=tenant.unique_domain)
    else:
        return redirect("core:tenant", tenant=tenant.unique_domain)


class DriverUpdateView(TenantAwareViewMixin, DetailView):
    model = fleet_models.Driver
    template_name = 'pages/tenant/fleet/driver_modif.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


def update_driver(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
    u_tenant: 'Tenant' = request.user.profile.tenant
    tenant = u_tenant

    if request.method != "POST":
        return redirect("core:tenant", tenant=tenant.unique_domain)

    # Getting datas from the form
    last_name = request.POST.get('last_name')
    first_name = request.POST.get('first_name')
    phone_number = request.POST.get('phone_number')
    license_number = request.POST.get('license_number')
    driver_license = request.FILES.get('driver_license')

    # Updating the corresponding car object
    driver = fleet_models.Driver.objects.filter(statut=True, id=type_id)[:1].get()
    driver.last_name = last_name
    driver.first_name = first_name
    driver.phone_number = phone_number
    driver.license_number = license_number
    driver.driver_license = driver_license
    driver.save()

    return redirect('core:tenant:fleet:driver_list', tenant=tenant.unique_domain)


def delete_driver(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
    tenant: 'Tenant' = request.user.profile.tenant
    tenant = tenant
    driver = fleet_models.Driver.objects.filter(statut=True, id=type_id)[:1].get()
    driver.delete()
    return redirect('core:tenant:fleet:driver_list', tenant=tenant.unique_domain)


class ContractListView(TenantAwareViewMixin, ListView):
    template_name = 'pages/tenant/fleet/contract_list.html'

    def get_queryset(self):
        return fleet_models.Contract.objects.filter(statut=True, tenant=self.tenant)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["drivers"] = fleet_models.Driver.objects.all()
        context["cars"] = fleet_models.Car.objects.all()
        context["week"] = core_models.DayOfTheWeek.objects.all()
        return context


class ContractDetailView(TenantAwareViewMixin, DetailView):
    model = fleet_models.Contract
    template_name = 'pages/tenant/fleet/contract_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["drivers"] = fleet_models.Driver.objects.all()
        context["cars"] = fleet_models.Car.objects.all()
        context["week"] = core_models.DayOfTheWeek.objects.all()
        return context


def add_contract(request: HttpRequest, tenant: str) -> HttpResponse:
    tenant: 'Tenant' = request.user.profile.tenant
    if request.method == "POST":
        driver = int(request.POST.get('driver'))
        car = int(request.POST.get('car'))
        expect_daily_revenue = request.POST.get('expect_daily_revenue')
        holiday_expect_revenu = request.POST.get('holiday_expect_revenu')
        rest_days = request.POST.getlist('rest_days')
        rest_days = [int(i) for i in rest_days]
        print("[] :", rest_days)
        is_active = request.POST.get('is_active')
        if is_active == 'on':
            is_active = True
        else:
            is_active = False

        contrat = fleet_models.Contract(
            driver_id=driver,
            car_id=car,
            expect_daily_revenue=expect_daily_revenue,
            holiday_expect_revenu=holiday_expect_revenu,
            is_active=True if is_active == 'on' else is_active != 'on',
            tenant=tenant
        )
        contrat.save()
        for day in rest_days:
            contrat.rest_days.add(day)
        contrat.save()

        return redirect('core:tenant:fleet:contract_list', tenant=tenant.unique_domain)
    else:
        return redirect("core:tenant", tenant=tenant.unique_domain)


class ContractUpdateView(TenantAwareViewMixin, DetailView):
    model = fleet_models.Contract
    template_name = 'pages/tenant/fleet/contract_modif.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["drivers"] = fleet_models.Driver.objects.all()
        context["cars"] = fleet_models.Car.objects.all()
        context["week"] = core_models.DayOfTheWeek.objects.all()
        return context


def update_contract(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
    u_tenant: 'Tenant' = request.user.profile.tenant
    tenant = u_tenant

    if request.method != "POST":
        return redirect("core:tenant", tenant=tenant.unique_domain)

    # Getting datas from the form
    car = int(request.POST.get('car'))
    driver = int(request.POST.get('driver'))
    expect_daily_revenue = request.POST.get('expect_daily_revenue')
    holiday_expect_revenu = request.POST.get('holiday_expect_revenu')
    rest_days = request.POST.getlist('rest_days')
    rest_days = [int(i) for i in rest_days]
    print("[] :", rest_days)
    is_active = request.POST.get('is_active')

    # Updating the corresponding car object
    contract = fleet_models.Contract.objects.filter(statut=True, id=type_id)[:1].get()
    contract.driver_id = driver
    contract.car_id = car
    contract.expect_daily_revenue = expect_daily_revenue
    contract.holiday_expect_revenu = holiday_expect_revenu
    if is_active == 'on':
        contract.is_active = True
    else:
        contract.is_active = False
    contract.save()
    for day in rest_days:
        contract.rest_days.add(day)
    contract.save()

    return redirect('core:tenant:fleet:contract_list', tenant=tenant.unique_domain)


def delete_contract(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
    tenant: 'Tenant' = request.user.profile.tenant
    tenant = tenant
    contract = fleet_models.Contract.objects.filter(statut=True, id=type_id)[:1].get()
    contract.delete()
    return redirect('core:tenant:fleet:contract_list', tenant=tenant.unique_domain)
