from django.urls import path, include
from core.views import tenant

app_name = 'tenant'

urlpatterns = [
	path('', main.index, name='home'),
	path('flotte/', include('fleet_app.urls.tenant'), name='fleet'),
]
