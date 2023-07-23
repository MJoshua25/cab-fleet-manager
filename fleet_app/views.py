from django.shortcuts import render

from fleet_app import models as fleet_models


def carGestion(request):
    data = {
       'cars': fleet_models.Car.objects.filter(statut=True)
    }
    return render(request, 'pages/fleet/carGestion.html', data)
