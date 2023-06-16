from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# from blog import models


def index(request):
	data = {
		'titre': "pade d'accueil",
		# 'cats': models.Categorie.objects.filter(status=True)
	}
	return render(request, 'pages/index.html', data)