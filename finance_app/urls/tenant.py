from django.urls import path, include
from finance_app.views import tenant

app_name = 'finance'

urlpatterns = [
	# Urls Insurance
	path('assurance', tenant.InsuranceListView.as_view(), name='insurance_list'),
	path('assurance/ajout_assurance', tenant.add_insurance, name='add_tenant_insurance'),
	path('assurance/<int:pk>', tenant.InsuranceDetailView.as_view(), name='insurance_detail'),
	path('assurance/modif_assurance/<int:pk>', tenant.InsuranceUpdateView.as_view(), name='insurance_update'),
	path('assurance/modifier_assurance/<int:type_id>', tenant.update_insurance, name='update_tenant_insurance'),
	path('assurance/supprimer_assurance/<int:type_id>', tenant.delete_insurance, name='delete_tenant_insurance'),
	# Urls Insurance Payment
	path('paiement_assurance', tenant.InsurancePaymentListView.as_view(), name='insurance_payment_list'),
	path('paiement_assurance/ajout_assurance', tenant.add_insurance_payment, name='add_tenant_insurance_payment'),
	path('paiement_assurance/<int:pk>', tenant.InsurancePaymentDetailView.as_view(), name='insurance_payment_detail'),
	path('paiement_assurance/modif_paiement_assurance/<int:pk>', tenant.InsurancePaymentUpdateView.as_view(),
	     name='insurance_payment_update'),
	path('paiement_assurance/modifier_paiement_assurance/<int:type_id>', tenant.update_insurance_payment,
	     name='update_tenant_insurance_payment'),
	path('paiement_assurance/supprimer_paiement_assurance/<int:type_id>', tenant.delete_insurance_payment,
	     name='delete_tenant_insurance_payment'),
	# Urls Outages
	path('panne', tenant.OutageListView.as_view(), name='outage_list'),
	path('panne/<int:outage_id>/modifier/', tenant.OutageUpdateView.as_view(), name='outage_update'),
	path('panne/<int:outage_id>/supprimer/', tenant.OutageDeleteView.as_view(), name='outage_delete'),
	# Urls OilChange
	path('vidange', tenant.OilChangeListView.as_view(), name='oil_change_list'),
	path('vidange/ajout_vidange', tenant.add_oil_change, name='add_tenant_oil_change'),
	path('vidange/<int:pk>', tenant.OilChangeDetailView.as_view(), name='oil_change_detail'),
	path('vidange/modif_vidange/<int:pk>', tenant.OilChangeUpdateView.as_view(), name='oil_change_update'),
	path('vidange/modifier_vidange/<int:type_id>', tenant.update_oil_change, name='update_tenant_oil_change'),
	path('vidange/supprimer_vidange/<int:type_id>', tenant.delete_oil_change, name='delete_tenant_oil_change'),
]
