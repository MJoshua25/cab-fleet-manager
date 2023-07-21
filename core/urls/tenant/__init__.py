from django.urls import path, include
from core.views import main

app_name = 'tenant'

urlpatterns = [
	path('', main.index, name='home'),
]