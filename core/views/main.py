from django.http import HttpResponseRedirect, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from tenant import models as tenant_models
from fleet_app import models as fleet_models
from django.db import transaction
from django.contrib.auth.models import User
from tenant.decorators import no_tenant_required
from core import models
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
import uuid
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


def forget_password(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        email = request.POST.get('email')
        token = str(uuid.uuid4())
        link = f"http://127.0.0.1:8000/change_password_user/{token}"
        subject = 'Bienvenue sur Fleet-Wise'
        email_from = settings.EMAIL_HOST_USER
        message = "Cher(e) Mr/Mme, trouvez ci-dessous le lien pour la réintialisation de votre mot de passe. \n" \
                  "[" + link + "]" \
                               "\n Cordialement," \
                               "L'équipe de Fleet-wise"
        recipient_list = [email]
        k = User.objects.get(email=email)
        print('k', k.email)
        if not k:
            print('Pas de mail correspondant')
            messages.error(request, "Pas de mail correspondant")
            return redirect('core:login')
        user_obj = User.objects.get(email=email)
        print('User', user_obj)
        profile_obj = fleet_models.FleetUser.objects.get(user=user_obj)
        print('profile', profile_obj)
        profile_obj.token_forget_password = token
        profile_obj.save()
        send_mail(subject, message, email_from, recipient_list, fail_silently=False)
        messages.success(request, "Email envoyé")
        return redirect("core:home")
    else:
        data = {

        }
        return render(request, 'pages/forget_password.html', data)


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
    if request.method != "POST":
        return redirect("core:home")
    password = request.POST.get('password')
    comfirm_password = request.POST.get('comfirmpassword')
    if password != comfirm_password:
        messages.error(request, "Mot de passe non identique")
        return redirect("core:home")

    user = request.user
    tenant = user.profile.tenant
    profile = user.profile

    user.set_password(password)
    profile.is_new = False
    user.save()
    profile.save()
    print("Update :", user.profile.is_new)
    auth_logout(request)
    return redirect("core:login")


def forget_password_user(request: HttpRequest, token: str) -> HttpResponse:
    if request.method == "POST":
        password = request.POST.get('password')
        comfirm_password = request.POST.get('comfirmpassword')
        user_id = request.POST.get('user_id')
        if user_id is None:
            print("Aucun utilisateur trouvé")
            return redirect("core:home")
        if password != comfirm_password:
            messages.error(request, "Mot de passe non identique")
            return redirect("core:forget_password", token)

        profil_obj = fleet_models.FleetUser.objects.filter(token_forget_password=token).first()
        data = {
            'user_id': profil_obj.user_id
        }
        user_obj = fleet_models.FleetUser.user.objects.get(id=user_id)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, "Mot de passe changé")
        return redirect("core:login", data)
    else:
        data = {
            'ft': fleet_models.FleetUser.objects.filter(statut=True)
        }
        return render(request, 'pages/forget_pass.html', data)


def logout(request):
    auth_logout(request)
    return redirect('core:home')
