from django.urls import path, include
from core.views import main

app_name = 'core'

urlpatterns = [
	path('', main.index, name='home'),
	path('connexion', main.login, name='login'),
	path('inscription', main.register, name='register'),
	path('change_password', main.change_password, name='change_password'),
	path('change_password_user', main.change_password_user, name='change_password_user'),
	path('ajout_tenant_utilisateur/', main.add_tenant_user, name='add_tenant_user'),
	path('valider_domaine/', main.validate_domain, name='validate_domain'),
	path('deconnexion/', main.logout, name='logout'),
	path('<str:tenant>/', include('core.urls.tenant'), name='tenant'),
]
