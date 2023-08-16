from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from fleet_app import models as fleet_models
from finance_app import models as finance_models
from core import models as core_models
from tenant.mixin import TenantAwareViewMixin
from tenant import models as tenant_models
from django.db import transaction
from django.utils import timezone
from fleet_app import forms as fleet_forms
import datetime
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from tenant.models import Tenant


class InsuranceListView(TenantAwareViewMixin, ListView):
    template_name = 'pages/tenant/finance/insurance_list.html'

    def get_queryset(self):
        return fleet_models.Insurance.objects.filter(statut=True, tenant=self.tenant)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["drivers"] = fleet_models.Driver.objects.all()
        context["cars"] = fleet_models.Car.objects.all()
        context["week"] = core_models.DayOfTheWeek.objects.all()
        return context


class InsuranceDetailView(TenantAwareViewMixin, DetailView):
    model = fleet_models.Insurance
    template_name = 'pages/tenant/finance/insurance_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["drivers"] = fleet_models.Driver.objects.all()
        context["cars"] = fleet_models.Car.objects.all()
        context["week"] = core_models.DayOfTheWeek.objects.all()
        return context


def add_insurance(request: HttpRequest, tenant: str) -> HttpResponse:
    tenant: 'Tenant' = request.user.profile.tenant
    if request.method == "POST":
        insurance_company = request.POST.get('insurance_company')
        car = int(request.POST.get('car'))

        due_date = request.POST.get('due_date')
        monthly_amount = request.POST.get('monthly_amount')
        last_payment = request.POST.get('monthly_amount')
        next_date = request.POST.get('due_date')
        print("Bdue_date", due_date)
        print("Bother", next_date)
        insurance = fleet_models.Insurance(
            car_id=car,
            insurance_company=insurance_company,
            monthly_amount=monthly_amount,
            due_date=datetime.datetime.strptime(due_date, '%Y-%m-%d  %H:%M').date(),
            last_payment=last_payment,
            next_date=datetime.datetime.strptime(next_date, '%Y-%m-%d  %H:%M').date(),
            tenant=tenant
        )
        print("due_date", due_date)
        print("other", next_date)
        insurance.save()

        return redirect('core:tenant:finance:insurance_list', tenant=tenant.unique_domain)
    else:
        return redirect("core:tenant", tenant=tenant.unique_domain)


class InsuranceUpdateView(TenantAwareViewMixin, DetailView):
    model = fleet_models.Insurance
    template_name = 'pages/tenant/finance/insurance_modif.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["drivers"] = fleet_models.Driver.objects.all()
        context["cars"] = fleet_models.Car.objects.all()
        context["week"] = core_models.DayOfTheWeek.objects.all()
        return context


def update_insurance(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
    u_tenant: 'Tenant' = request.user.profile.tenant
    tenant = u_tenant

    if request.method != "POST":
        return redirect("core:tenant", tenant=tenant.unique_domain)

    # Getting datas from the form
    car = int(request.POST.get('car'))
    insurance_company = request.POST.get('insurance_company')
    due_date = request.POST.get('due_date')
    monthly_amount = request.POST.get('monthly_amount')
    last_payment = request.POST.get('monthly_amount')
    next_date = request.POST.get('due_date')
    print("Bdue_date", due_date)
    print("Bother", next_date)
    # Updating the corresponding car object
    insurance = fleet_models.Insurance.objects.filter(statut=True, id=type_id)[:1].get()
    insurance.car_id = car
    insurance.insurance_company = insurance_company
    insurance.due_date = str(due_date)
    insurance.monthly_amount = monthly_amount
    insurance.last_payment = last_payment
    insurance.next_date = str(next_date)
    print("due_date", insurance.due_date)
    print("other", insurance.next_date)
    insurance.save()

    return redirect('core:tenant:finance:insurance_list', tenant=tenant.unique_domain)


def delete_insurance(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
    tenant: 'Tenant' = request.user.profile.tenant
    tenant = tenant
    contract = fleet_models.Insurance.objects.filter(statut=True, id=type_id)[:1].get()
    contract.delete()
    return redirect('core:tenant:finance:insurance_list', tenant=tenant.unique_domain)

