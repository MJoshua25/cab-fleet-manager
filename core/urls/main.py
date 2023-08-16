from django.urls import path, include
from core.views import main

app_name = 'core'

urlpatterns = [
	path('', main.index, name='home'),
	path('connexion', main.login, name='login'),
	path('inscription', main.register, name='register'),
	path('ajout_tenant_utilisateur/', main.add_tenant_user, name='add_tenant_user'),
	path('valider_domaine/', main.validate_domain, name='validate_domain'),
	path('deconnexion/', main.logout, name='logout'),
	path('<str:tenant>/', include('core.urls.tenant'), name='tenant'),
]
