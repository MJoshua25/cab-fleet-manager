from django.urls import path, include
from core.views import main

app_name = 'core'

urlpatterns = [
	path('', main.index, name='home'),
	path('login', main.login, name='login'),
	path('register', main.register, name='register'),
	path('<str:tenant>/', include('core.urls.tenant')),
]
