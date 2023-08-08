from django.urls import path, include
from fleet_app.views import tenant

app_name = 'fleet'

urlpatterns = [
    # Urls Vehicule
    path('vehicule', tenant.CarListView.as_view(), name='car_list'),
    path('vehicule/ajout_vehicule', tenant.add_vehicule, name='add_tenant_vehicule'),
    path('vehicule/<int:pk>', tenant.CarDetailView.as_view(), name='car_detail'),
    path('vehicule/modif_vehicule/<int:pk>', tenant.CarUpdateView.as_view(), name='car_update'),
    path('vehicule/modifier_vehicule/<int:type_id>', tenant.update_vehicule, name='update_tenant_vehicule'),
    path('vehicule/supprimer_vehicule/<int:type_id>', tenant.delete_vehicule, name='delete_tenant_vehicule'),
    # Urls Chauffeur
    path('chauffeur', tenant.DriverListView.as_view(), name='driver_list'),
    # Urls Contract
    path('contrat', tenant.ContractListView.as_view(), name='contract_list'),

]
