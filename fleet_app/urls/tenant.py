from django.urls import path, include
from core.views import main
from fleet_app.views import tenant
app_name = 'fleet'

urlpatterns = [
	path('vehicule', tenant.carGestion, name='carGestion'),
	path('chauffeur', tenant.driverGestion, name='driverGestion'),
	path('contrat', tenant.contratGestion, name='contratGestion'),
]