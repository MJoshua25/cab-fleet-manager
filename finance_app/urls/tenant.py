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
    #Urls Insurance Payment
    path('paiement_assurance', tenant.InsurancePaymentListView.as_view(), name='insurance_payment_list'),
    path('paiement_assurance/ajout_assurance', tenant.add_insurance_payment, name='add_tenant_insurance_payment'),
    path('paiement_assurance/<int:pk>', tenant.InsurancePaymentDetailView.as_view(), name='insurance_payment_detail'),
    path('paiement_assurance/modif_paiement_assurance/<int:pk>', tenant.InsurancePaymentUpdateView.as_view, name='insurance_payment_update'),
    path('paiement_assurance/modifier_paiement_assurance/<int:type_id>', tenant.update_insurance_payment, name='update_tenant_insurance_payment'),
    path('paiement_assurance/supprimer_paiement_assurance/<int:type_id>', tenant.delete_insurance_payment, name='delete_tenant_insurance_payment'),
]
