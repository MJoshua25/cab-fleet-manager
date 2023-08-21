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
		context["drivers"] = fleet_models.Driver.objects.all()
		context["cars"] = fleet_models.Car.objects.all()
		context["week"] = core_models.DayOfTheWeek.objects.all()
		context["insurance"] = fleet_models.Insurance.objects.all()
		context["contract"] = fleet_models.Contract.objects.all()
		context["expense"] = finance_models.Expense.objects.all()
		return context


class InsurancePaymentDetailView(TenantAwareViewMixin, DetailView):
	model = fleet_models.InsurancePayment
	template_name = 'pages/tenant/finance/insurance_payment_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["drivers"] = fleet_models.Driver.objects.all()
		context["cars"] = fleet_models.Car.objects.all()
		context["week"] = core_models.DayOfTheWeek.objects.all()
		context["insurance"] = fleet_models.Insurance.objects.all()
		context["contract"] = fleet_models.Contract.objects.all()
		context["expense"] = finance_models.Expense.objects.all()
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
		context["drivers"] = fleet_models.Driver.objects.all()
		context["cars"] = fleet_models.Car.objects.all()
		context["week"] = core_models.DayOfTheWeek.objects.all()
		context["insurance"] = fleet_models.Insurance.objects.all()
		context["contract"] = fleet_models.Contract.objects.all()
		context["expense"] = finance_models.Expense.objects.all()
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


class OutageListView(TenantAwareViewMixin, ListView):
	template_name = 'pages/tenant/finance/outage/outage_list.html'
	form_class = finance_app_forms.outage.OutageForm

	def get_queryset(self):
		return fleet_models.Outage.objects.filter(statut=True, tenant=self.tenant).order_by('is_okay', '-date_payment')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["drivers"] = fleet_models.Driver.objects.filter(statut=True, tenant=self.tenant)
		context["cars"] = fleet_models.Car.objects.filter(statut=True, tenant=self.tenant)
		context["reasons"] = fleet_models.OutageReason.objects.filter(statut=True)
		context["tenant"] = self.tenant
		return context

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			outage = form.save()
		return self.get(request, *args, **kwargs)


class OutageUpdateView(TenantAwareViewMixin, View):
	form_class = finance_app_forms.outage.OutageForm

	def post(self, request, *args, **kwargs):
		outage_id = kwargs.get('outage_id', None)
		if not outage_id:
			return redirect('core:tenant:finance:outage_list')
		outage = fleet_models.Outage.objects.filter(pk=outage_id).first()
		if not outage:
			return redirect('core:tenant:finance:outage_list')
		form = self.form_class(request.POST, instance=outage)
		if form.is_valid():
			form.save()
		return redirect('core:tenant:finance:outage_list')


class OutageDeleteView(TenantAwareViewMixin, View):

	def get(self, request, *args, **kwargs):
		outage_id = kwargs.get('outage_id', None)
		if not outage_id:
			return redirect('core:tenant:finance:outage_list')
		outage = fleet_models.Outage.objects.filter(pk=outage_id).first()
		if not outage:
			return redirect('core:tenant:finance:outage_list')
		outage.delete()
		return redirect('core:tenant:finance:outage_list')
