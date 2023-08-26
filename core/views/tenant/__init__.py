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
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
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
    subject = 'Bienvenue sur Fleet-Wise'
    email_from = settings.EMAIL_HOST_USER
    if request.method == "POST":
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        message = "Cher(e) Mr/Mme, " \
                  "Nous sommes ravis de vous accueillir dans notre Application de Gestion de Flotte ! Votre compte a été créé avec succès et vous êtes prêt(e) à commencer à gérer efficacement votre flotte de véhicules. " \
                  "Voici vos informations de connexion :" \
                  "Mot de passe : [ " + password + "]." \
                  "Nous vous recommandons vivement de changer votre mot de passe dès votre première connexion pour des raisons de sécurité." \
                  "Nous vous remercions de faire confiance à notre application pour la gestion de votre flotte. " \
                  "Nous sommes impatients de vous aider à optimiser vos opérations et à tirer le meilleur parti de notre solution." \
                  "Bienvenue à bord !" \
                  "Cordialement," \
                  "L'équipe de Fleet-WIse"
        recipient_list = [email]
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
            is_new=True
        )
        print("Fleet :", fleet_user.is_new)
        with transaction.atomic():
            u.set_password(u.password)
            u.save()
            fleet_user.save()

        send_mail(subject, message, email_from, recipient_list, fail_silently=False,)
        messages.success(request, "Ajout d'utilisateur éffectué")
        return redirect("core:tenant:user_management", tenant=tenant.unique_domain)
    else:
        messages.error(request, "Ajout d'utilisateur non éffectué ")
        return redirect("core:tenant:user_management", tenant=tenant.unique_domain)


def delete_user(request: HttpRequest, tenant: str, type_id: int) -> HttpResponse:
    tenant: 'Tenant' = request.user.profile.tenant
    tenant = tenant
    fleet_user = fleet_app_models.FleetUser.objects.filter(statut=True, id=type_id)[:1].get()
    fleet_user.user.delete()
    messages.success(request, "Suppression d'un utilisateur éffectué")
    return redirect('core:tenant:user_management', tenant=tenant.unique_domain)

