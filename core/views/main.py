from django.http import HttpResponseRedirect, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from tenant import models as tenant_models
from fleet_app import models as fleet_models
from django.db import transaction
from tenant.decorators import no_tenant_required
from core import models
from django.contrib import messages

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from core.forms.auth import LoginForm
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from tenant.models import Tenant


def index(request: HttpRequest) -> HttpResponse:
    data = {
        'titre': "page d'accueil",
        # 'cats': models.Categorie.objects.filter(status=True)
    }
    return render(request, 'pages/index.html', data)


@no_tenant_required
def register(request: HttpRequest) -> HttpResponse:
    print("started")
    data = {
        'titre': "pade d'accueil",
        # 'cats': models.Categorie.objects.filter(status=True)
    }
    print("ended")
    return render(request, 'pages/register.html', data)


def add_tenant_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        name = request.POST.get('name')
        unique_domain = request.POST.get('unique_domain')
        lastname = request.POST.get('lastname')
        firstname = request.POST.get('firstname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact = request.POST.get('tel')
        password = request.POST.get('formValidationPass')
        # TODO: Valider les donner avant de continuer
        add_tenant = tenant_models.Tenant(
            name=name,
            unique_domain=unique_domain
        )
        u = fleet_models.User(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            password=password
        )
        fleet_user = fleet_models.FleetUser(
            user=u,
            tenant=add_tenant,
            contact=contact,
        )
        with transaction.atomic():
            add_tenant.save()
            u.set_password(u.password)
            u.save()
            fleet_user.save()
        return redirect("core:tenant:home", tenant=add_tenant.unique_domain)
    else:
        return redirect("core:home")


@no_tenant_required
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user is not None and hasattr(user, 'profile'):
                auth_login(request, user)
                print('CO : ', user.profile.is_new)
                if user.profile.is_new:
                    print('CO1 : ', user.profile.is_new)
                    return redirect('core:change_password')
                else:
                    tenant = user.profile.tenant
                    return redirect('core:tenant:home', tenant=tenant.unique_domain)
    data = {
        'titre': "page de connexion",
        # 'cats': models.Categorie.objects.filter(status=True)
    }
    return render(request, 'pages/login.html', data)


def validate_domain(request):
    unique_domain = request.POST.get('unique_domain', None)
    data = {
        'is_taken': tenant_models.Tenant.objects.filter(unique_domain=unique_domain).exists()
    }
    return JsonResponse(data)


def change_password(request: HttpRequest) -> HttpResponse:
    data = {
    }
    print("ended")
    return render(request, 'pages/update_password.html', data)


def change_password_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user = request.user
        password = request.POST.get('password')
        comfirmpassword = request.POST.get('comfirmpassword')
        if password != comfirmpassword:
            messages.error(request, "Mot de passe non identique")
            return redirect("core:home")
        else:
            tenant = user.profile.tenant
            user.set_password(password)
            user.profile.is_new = False
            user.save()
            print("Update :", user.profile.is_new)
            return redirect("core:login")


def logout(request):
    auth_logout(request)
    return redirect('core:home')
