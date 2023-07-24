from django.shortcuts import render

from fleet_app import models as fleet_models


def carGestion(request):
    data = {
        'cars': fleet_models.Car.objects.filter(statut=True)
    }
    return render(request, 'pages/fleet/carGestion.html', data)


def driverGestion(request):
    data = {
        'drivers': fleet_models.Driver.objects.filter(statut=True)
    }
    return render(request, 'pages/fleet/driverGestion.html', data)


def contratGestion(request):
    data = {
        'contrats': fleet_models.Contract.objects.filter(statut=True)
    }
    return render(request, 'pages/fleet/contractGestion.html', data)
