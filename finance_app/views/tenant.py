from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from fleet_app import models as fleet_models
from finance_app import models as finance_models
from core import models as core_models
from tenant.mixin import TenantAwareViewMixin
from finance_app import forms as finance_app_forms
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
		context["drivers"] = fleet_models.Driver.objects.filter(tenant=self.tenant, statut=True)
		context["cars"] = fleet_models.Car.objects.filter(tenant=self.tenant, statut=True)
		context["week"] = core_models.DayOfTheWeek.objects.filter(tenant=self.tenant, statut=True)
		return context


class InsuranceDetailView(TenantAwareViewMixin, DetailView):
	model = fleet_models.Insurance
	template_name = 'pages/tenant/finance/insurance_detail.html'


def get_context_data(self, **kwargs):
	context = super().get_context_data(**kwargs)
	context["drivers"] = fleet_models.Driver.objects.filter(tenant=self.tenant, statut=True)
	context["cars"] = fleet_models.Car.objects.filter(tenant=self.tenant, statut=True)
	context["week"] = core_models.DayOfTheWeek.objects.filter(tenant=self.tenant, statut=True)
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
			due_date=datetime.datetime.strptime(due_date, '%Y-%m-%dT%H:%M').date(),
			last_payment=last_payment,
			next_date=datetime.datetime.strptime(next_date, '%Y-%m-%dT%H:%M').date(),
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
	context["drivers"] = fleet_models.Driver.objects.filter(tenant=self.tenant, statut=True)
	context["cars"] = fleet_models.Car.objects.filter(tenant=self.tenant, statut=True)
	context["week"] = core_models.DayOfTheWeek.objects.filter(tenant=self.tenant, statut=True)
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
	insurance.due_date = datetime.datetime.strptime(due_date, '%Y-%m-%dT%H:%M').date()
	insurance.due_date = str(insurance.due_date)
	insurance.monthly_amount = monthly_amount
	insurance.last_payment = last_payment
	insurance.next_date = datetime.datetime.strptime(next_date, '%Y-%m-%dT%H:%M').date()
	insurance.next_date = str(insurance.next_date)
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


class InsurancePaymentListView(TenantAwareViewMixin, ListView):
	template_name = 'pages/tenant/finance/insurance_payment_list.html'

	def get_queryset(self):
		return fleet_models.InsurancePayment.objects.filter(statut=True, tenant=self.tenant)


def get_context_data(self, **kwargs):
	context = super().get_context_data(**kwargs)
	context["drivers"] = fleet_models.Driver.objects.filter(tenant=self.tenant, statut=True)
	context["cars"] = fleet_models.Car.objects.filter(tenant=self.tenant, statut=True)
	context["week"] = core_models.DayOfTheWeek.objects.filter(statut=True)
	context["insurance"] = fleet_models.Insurance.objects.filter(tenant=self.tenant, statut=True)
	context["contract"] = fleet_models.Contract.objects.filter(tenant=self.tenant, statut=True)
	context["expense"] = finance_models.Expense.objects.filter(tenant=self.tenant, statut=True)
	return context


class InsurancePaymentDetailView(TenantAwareViewMixin, DetailView):
	model = fleet_models.InsurancePayment
	template_name = 'pages/tenant/finance/insurance_payment_detail.html'


def get_context_data(self, **kwargs):
	context = super().get_context_data(**kwargs)
	context["drivers"] = fleet_models.Driver.objects.filter(tenant=self.tenant, statut=True)
	context["cars"] = fleet_models.Car.objects.filter(tenant=self.tenant, statut=True)
	context["week"] = core_models.DayOfTheWeek.objects.filter(statut=True)
	context["insurance"] = fleet_models.Insurance.objects.filter(tenant=self.tenant, statut=True)
	context["contract"] = fleet_models.Contract.objects.filter(tenant=self.tenant, statut=True)
	context["expense"] = finance_models.Expense.objects.filter(tenant=self.tenant, statut=True)
	return context


def add_insurance_payment(request: HttpRequest, tenant: str) -> HttpResponse:
	tenant: 'Tenant' = request.user.profile.tenant
	if request.method == "POST":
		amount = request.POST.get('amount')
		payment_method = request.POST.get('payment_method')
		date_payment = request.POST.get('date_payment')
		insurance = int(request.POST.get('insurance'))
		contract = int(request.POST.get('contract'))
		is_sold_out = request.POST.get('is_sold_out')
		if is_sold_out == 'on':
			is_sold_out = True
		else:
			is_sold_out = False
		i = fleet_models.InsurancePayment(
			insurance_id=insurance,
			contract_id=contract,
			is_sold_out=True if is_sold_out == 'on' else is_sold_out != 'on',
			amount=amount,
			payment_method=payment_method,
			date_payment=datetime.datetime.strptime(date_payment, '%Y-%m-%dT%H:%M').date(),
			tenant=tenant
		)
		i.save()
		return redirect('core:tenant:finance:insurance_payment_list', tenant=tenant.unique_domain)
	else:
		return redirect("core:tenant", tenant=tenant.unique_domain)


class InsurancePaymentUpdateView(TenantAwareViewMixin, DetailView):
	model = fleet_models.InsurancePayment
	template_name = 'pages/tenant/finance/insurance_payment_modif.html'


def get_context_data(self, **kwargs):
	context = super().get_context_data(**kwargs)
	context["drivers"] = fleet_models.Driver.objects.filter(tenant=self.tenant, statut=True)
	context["cars"] = fleet_models.Car.objects.filter(tenant=self.tenant, statut=True)
	context["week"] = core_models.DayOfTheWeek.objects.filter(statut=True)
	context["insurance"] = fleet_models.Insurance.objects.filter(tenant=self.tenant, statut=True)
	context["contract"] = fleet_models.Contract.objects.filter(tenant=self.tenant, statut=True)
	context["expense"] = finance_models.Expense.objects.filter(tenant=self.tenant, statut=True)
	return context


def update_insurance_payment(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
	u_tenant: 'Tenant' = request.user.profile.tenant
	tenant = u_tenant

	if request.method != "POST":
		return redirect("core:tenant", tenant=tenant.unique_domain)

	# Getting datas from the form
	amount = request.POST.get('amount')
	payment_method = request.POST.get('payment_method')
	date_payment = request.POST.get('date_payment')
	insurance = int(request.POST.get('insurance'))
	contract = int(request.POST.get('contract'))
	is_sold_out = request.POST.get('is_sold_out')
	print('Bfdate_payment', date_payment)
	if is_sold_out == 'on':
		is_sold_out = True
	else:
		is_sold_out = False
	# Updating the corresponding car object
	i_payment = fleet_models.InsurancePayment.objects.filter(statut=True, id=type_id)[:1].get()
	i_payment.amount = amount
	i_payment.payment_method = payment_method
	i_payment.date_payment = datetime.datetime.strptime(date_payment, '%Y-%m-%dT%H:%M').date()
	i_payment.date_payment = str(i_payment.date_payment)
	print('Afdate_payment', i_payment.date_payment)
	i_payment.insurance_id = insurance
	i_payment.contract_id = contract
	if is_sold_out == 'on':
		i_payment.is_sold_out = True
	else:
		i_payment.is_sold_out = False

	i_payment.save()
	return redirect('core:tenant:finance:insurance_payment_list', tenant=tenant.unique_domain)


def delete_insurance_payment(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
	tenant: 'Tenant' = request.user.profile.tenant
	tenant = tenant
	contract = fleet_models.InsurancePayment.objects.filter(statut=True, id=type_id)[:1].get()
	contract.delete()
	return redirect('core:tenant:finance:insurance_payment_list', tenant=tenant.unique_domain)


class OilChangeListView(TenantAwareViewMixin, ListView):
	template_name = 'pages/tenant/finance/oil_change_list.html'

	def get_queryset(self):
		return fleet_models.OilChange.objects.filter(statut=True, tenant=self.tenant)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["drivers"] = fleet_models.Driver.objects.filter(tenant=self.tenant, statut=True)
		context["cars"] = fleet_models.Car.objects.filter(tenant=self.tenant, statut=True)
		context["week"] = core_models.DayOfTheWeek.objects.filter(tenant=self.tenant, statut=True)
		context["insurance"] = fleet_models.Insurance.objects.filter(tenant=self.tenant, statut=True)
		context["contract"] = fleet_models.Contract.objects.filter(tenant=self.tenant, statut=True)
		context["expense"] = finance_models.Expense.objects.filter(tenant=self.tenant, statut=True)
		return context


class OilChangeDetailView(TenantAwareViewMixin, DetailView):
	model = fleet_models.OilChange
	template_name = 'pages/tenant/finance/oil_change_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["drivers"] = fleet_models.Driver.objects.filter(tenant=self.tenant, statut=True)
		context["cars"] = fleet_models.Car.objects.filter(tenant=self.tenant, statut=True)
		context["week"] = core_models.DayOfTheWeek.objects.filter(tenant=self.tenant, statut=True)
		context["insurance"] = fleet_models.Insurance.objects.filter(tenant=self.tenant, statut=True)
		context["contract"] = fleet_models.Contract.objects.filter(tenant=self.tenant, statut=True)
		context["expense"] = finance_models.Expense.objects.filter(tenant=self.tenant, statut=True)
		return context


def add_oil_change(request: HttpRequest, tenant: str) -> HttpResponse:
	tenant: 'Tenant' = request.user.profile.tenant
	if request.method == "POST":
		amount = request.POST.get('amount')
		payment_method = request.POST.get('payment_method')
		date_payment = request.POST.get('date_payment')
		oil_type = request.POST.get('oil_type')
		car = int(request.POST.get('car'))
		service_center = request.POST.get('service_center')
		date_OilChange = request.POST.get('date_OilChange')
		date_next_oil_change = request.POST.get('date_next_oil_change')
		i = fleet_models.OilChange(
			car_id=car,
			amount=amount,
			payment_method=payment_method,
			oil_type=oil_type,
			date_payment=datetime.datetime.strptime(date_payment, '%Y-%m-%dT%H:%M').date(),
			service_center=service_center,
			date_OilChange=datetime.datetime.strptime(date_OilChange, '%Y-%m-%dT%H:%M').date(),
			date_next_oil_change=datetime.datetime.strptime(date_next_oil_change, '%Y-%m-%dT%H:%M').date(),
			tenant=tenant
		)
		i.save()
		return redirect('core:tenant:finance:oil_change_list', tenant=tenant.unique_domain)
	else:
		return redirect("core:tenant", tenant=tenant.unique_domain)


class OilChangeUpdateView(TenantAwareViewMixin, DetailView):
	model = fleet_models.OilChange
	template_name = 'pages/tenant/finance/oil_change_modif.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["drivers"] = fleet_models.Driver.objects.filter(tenant=self.tenant, statut=True)
		context["cars"] = fleet_models.Car.objects.filter(tenant=self.tenant, statut=True)
		context["week"] = core_models.DayOfTheWeek.objects.filter(tenant=self.tenant, statut=True)
		context["insurance"] = fleet_models.Insurance.objects.filter(tenant=self.tenant, statut=True)
		context["contract"] = fleet_models.Contract.objects.filter(tenant=self.tenant, statut=True)
		context["expense"] = finance_models.Expense.objects.filter(tenant=self.tenant, statut=True)
		return context


def update_oil_change(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
	u_tenant: 'Tenant' = request.user.profile.tenant
	tenant = u_tenant

	if request.method != "POST":
		return redirect("core:tenant", tenant=tenant.unique_domain)

	# Getting datas from the form
	amount = request.POST.get('amount')
	payment_method = request.POST.get('payment_method')
	date_payment = request.POST.get('date_payment')
	car = int(request.POST.get('car'))
	oil_type = request.POST.get('oil_type')
	service_center = request.POST.get('service_center')
	date_OilChange = request.POST.get('date_OilChange')
	date_next_oil_change = request.POST.get('date_next_oil_change')

	# Updating the corresponding car object
	oilchange = fleet_models.OilChange.objects.filter(statut=True, id=type_id)[:1].get()
	oilchange.amount = amount
	oilchange.payment_method = payment_method
	oilchange.date_payment = datetime.datetime.strptime(date_payment, '%Y-%m-%dT%H:%M').date()
	oilchange.date_payment = str(oilchange.date_payment)
	oilchange.car_id = car
	oilchange.service_center = service_center
	oilchange.oil_type = oil_type
	oilchange.date_OilChange = datetime.datetime.strptime(date_OilChange, '%Y-%m-%dT%H:%M').date()
	oilchange.date_OilChange = str(oilchange.date_OilChange)
	oilchange.date_next_oil_change = datetime.datetime.strptime(date_next_oil_change, '%Y-%m-%dT%H:%M').date()
	oilchange.date_next_oil_change = str(oilchange.date_next_oil_change)

	oilchange.save()
	return redirect('core:tenant:finance:oil_change_list', tenant=tenant.unique_domain)


def delete_oil_change(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
	tenant: 'Tenant' = request.user.profile.tenant
	tenant = tenant
	oilchange = fleet_models.OilChange.objects.filter(statut=True, id=type_id)[:1].get()
	oilchange.delete()
	return redirect('core:tenant:finance:oil_change_list', tenant=tenant.unique_domain)
