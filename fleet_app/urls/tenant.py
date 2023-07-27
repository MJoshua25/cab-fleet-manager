from django.urls import path, include
from fleet_app.views import tenant
app_name = 'fleet'

urlpatterns = [
	path('vehicule', tenant.CarListView.as_view(), name='car_list'),
	path('chauffeur', tenant.DriverListView.as_view(), name='driver_list'),
	path('contrat', tenant.ContractListView.as_view(), name='contract_list'),
]