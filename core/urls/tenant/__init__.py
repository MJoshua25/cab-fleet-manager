from django.urls import path, include
from core.views import tenant

app_name = 'tenant'

urlpatterns = [
	path('', tenant.IndexView.as_view(), name='home'),
	path('profil/', tenant.UserProfileView.as_view(), name='user_profil'),
	path('utilisateur/Gestion des utilisateurs', tenant.UserListView.as_view(), name='user_management'),
	path('utilisateur/ajout_utilisateur', tenant.add_new_user, name='add_tenant_user'),
	path('utilisateur/supprimer_utilisateur/<int:type_id>', tenant.delete_user, name='delete_tenant_user'),
	path('flotte/', include('fleet_app.urls.tenant'), name='fleet'),
	path('finance/', include('finance_app.urls.tenant'), name='finance'),
]
