from django.urls import path, include
from core.views import tenant

app_name = 'tenant'

urlpatterns = [
	path('', tenant.IndexView.as_view(), name='home'),
	path('profil/', tenant.UserProfileView.as_view(), name='user_profil'),
	path('flotte/', include('fleet_app.urls.tenant'), name='fleet'),
	path('finance/', include('finance_app.urls.tenant'), name='finance'),
]
