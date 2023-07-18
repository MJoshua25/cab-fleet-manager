from django.contrib.auth import models
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from tenant import models as tenant_models
from fleet_app import models as fleet_models

# from blog import models


def index(request):
    data = {
        'titre': "pade d'accueil",
        # 'cats': models.Categorie.objects.filter(status=True)
    }
    return render(request, 'pages/index.html', data)


def login(request):
    data = {
        'titre': "pade d'accueil",
        # 'cats': models.Categorie.objects.filter(status=True)
    }
    return render(request, 'pages/login.html', data)


def register(request):
    data = {
        'titre': "pade d'accueil",
        # 'cats': models.Categorie.objects.filter(status=True)
    }
    return render(request, 'pages/register.html', data)


def addTenantUser(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        name = request.POST.get('name')
        uniqdomain = request.POST.get('uniqdomain')
        lastname = request.POST.get('lastname')
        firstname = request.POST.get('firstname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        add_tenant = tenant_models.Tenant(
            name=name,
            unique_domain=uniqdomain
        )
        u = models.User(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            password=password
        )
        add_fleetUser = fleet_models.FleetUser(
            user=u,
            contact=contact,
        )
        add_tenant.save()
        add_fleetUser.save()
        return redirect("core:home")
    else:
        return redirect("core:home")
