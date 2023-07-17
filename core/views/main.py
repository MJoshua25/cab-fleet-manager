from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
# from blog import models


def index(request):
	data = {
		'titre': "page d'accueil",
		# 'cats': models.Categorie.objects.filter(status=True)
	}
	return render(request, 'pages/index.html', data)


def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username and password:
			user = authenticate(username=username, password=password)
			if hasattr(user, 'profile'):
				tenant = user.profile.tenant
				return redirect('core:tenant:home', tenant=tenant)
	data = {
		'titre': "page de connexion",
		# 'cats': models.Categorie.objects.filter(status=True)
	}
	return render(request, 'pages/login.html', data)


def register(request):
	data = {
		'titre': "page d'inscription",
		# 'cats': models.Categorie.objects.filter(status=True)
	}
	return render(request, 'pages/register.html', data)

