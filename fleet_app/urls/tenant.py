from django.urls import path, include
from fleet_app.views import tenant
app_name = 'fleet'

urlpatterns = [
	path('vehicule', tenant.CarListView.as_view(), name='car_list'),
	path('chauffeur', tenant.DriverListView.as_view(), name='driver_list'),
	path('contrat', tenant.ContractListView.as_view(), name='contract_list'),
	path('vehicule/ajout_vehicule', tenant.add_vehicule, name='add_tenant_vehicule'),
	path('vehicule/<int:id_art>', tenant.CarDetailView.as_view(), name='car_detail'),

]