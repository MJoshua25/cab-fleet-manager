from django.urls import path, include
from core.views import main
from . import views
app_name = 'fleet'

urlpatterns = [
	path('carGestion', views.carGestion, name='carGestion'),
	path('driverGestion', views.driverGestion, name='driverGestion'),
	path('contratGestion', views.contratGestion, name='contratGestion'),
]
