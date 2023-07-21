from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


def index(request, tenant):
	print(tenant)
	data = {
		'titre': "page d'accueil",
		# 'cats': models.Categorie.objects.filter(status=True)
	}
	return render(request, 'pages/tenant/index.html', data)
