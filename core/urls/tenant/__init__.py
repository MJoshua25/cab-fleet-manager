from django.urls import path, include
from core.views import tenant

app_name = 'tenant'

urlpatterns = [
	path('', tenant.index, name='home'),
]
