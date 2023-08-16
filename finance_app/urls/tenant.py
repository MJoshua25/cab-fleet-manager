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

]
