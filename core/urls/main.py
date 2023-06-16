from django.urls import path, include
from core.views import main

app_name = 'core'

urlpatterns = [
	path('', main.index, name='home'),
]
