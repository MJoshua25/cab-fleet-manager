from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from tenant.mixin import TenantAwareViewMixin
from django.views.generic import ListView, DetailView
from fleet_app import models as fleet_app_models
from typing import TYPE_CHECKING, Union
from django.db import transaction
import secrets
import string
from django.contrib import messages

if TYPE_CHECKING:
    from tenant.models import Tenant


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


class UserListView(TenantAwareViewMixin, ListView):
    template_name = 'pages/tenant/user_management.html'

    def get_queryset(self):
        return fleet_app_models.FleetUser.objects.filter(statut=True, tenant=self.tenant)


def add_new_user(request: HttpRequest, tenant: str) -> HttpResponse:
    u_tenant: 'Tenant' = request.user.profile.tenant
    tenant = u_tenant
    if request.method == "POST":
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        u = fleet_app_models.User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        fleet_user = fleet_app_models.FleetUser(
            user=u,
            tenant=tenant,
            contact=contact,
        )
        with transaction.atomic():
            u.set_password(u.password)
            u.save()
            fleet_user.save()

        messages.success(request, "Vous venez d'ajouter un utilisateur ")
        return redirect("core:tenant:user_management", tenant=tenant.unique_domain)
    else:
        messages.error(request, "Ajout d'utilisateur non éffectué ")
        return redirect("core:tenant:user_management", tenant=tenant.unique_domain)


def delete_user(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
    tenant: 'Tenant' = request.user.profile.tenant
    tenant = tenant
    fleet_user = fleet_app_models.FleetUser.objects.filter(statut=True, id=type_id)[:1].get()
    fleet_user.delete()
    messages.success(request, "Suppression d'un utilisateur éffectué")
    return redirect('core:tenant:user_management', tenant=tenant.unique_domain)

