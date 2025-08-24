from django.http import HttpResponseRedirect, HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from tenant import models as tenant_models
from fleet_app import models as fleet_models
from django.db import transaction
from django.contrib.auth.models import User
from tenant.decorators import no_tenant_required
from core import models as core_models
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
import uuid
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from core.forms.auth import LoginForm
from core import functions as core_functions
from django.core.validators import validate_email
from typing import TYPE_CHECKING, Union
from django.views.decorators.http import require_GET

if TYPE_CHECKING:
	from tenant.models import Tenant


def index(request: HttpRequest) -> HttpResponse:
	data = {
		'titre': "page d'accueil",
		# 'cats': models.Categorie.objects.filter(status=True)
	}
	return render(request, 'pages/index.html', data)

@require_GET
def health_check(request):
	"""
	Health check endpoint for Docker/nginx. Returns HTTP 200 if the app is running.
	"""
	return JsonResponse({"status": "ok"}, status=200)


class ForgetPasswordView(TemplateView):
	template_name = 'pages/forget_password.html'

	def post(self, request, *args, **kwargs):
		email = request.POST.get('email')
		try:
			validate_email(email)
		except:
			messages.error(request, "Email non valide")
			return self.get(request, *args, **kwargs)

		user = User.objects.filter(email=email).first()
		if user is None:
			messages.error(request, "Pas de mail correspondant")
			return self.get(request, *args, **kwargs)

		token = str(uuid.uuid4())
		url = reverse("core:forget_password_user", args=(token,))
		base = core_functions.get_current_host(request)
		full_url = base + url
		profile = user.profile
		profile.token_forget_password = token
		profile.save()

		# Email details
		subject = 'Bienvenue sur Fleet-Wise'
		email_from = settings.EMAIL_HOST_USER
		message = "Cher(e) Mr/Mme, trouvez ci-dessous le lien pour la réintialisation de votre mot de passe. \n" \
		          "[" + full_url + "]" \
		                           "\n Cordialement," \
		                           "L'équipe de Fleet-wise"
		recipient_list = [email]
		send_mail(subject, message, email_from, recipient_list, fail_silently=False)

		messages.success(request, "Email envoyé")
		return redirect("core:home")


class ForgetPasswordUserView(TemplateView):
	template_name = 'pages/forget_pass.html'
	token = None
	user = None

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["token"] = self.token
		return context

	def dispatch(self, request, *args, **kwargs):
		token = kwargs.get('token', None)

		if not token:
			return redirect('core:home')

		user = User.objects.filter(profile__token_forget_password=token).first()

		if user is None:
			return redirect('core:home')

		self.user = user
		self.token = token
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		password = request.POST.get('password')
		comfirm_password = request.POST.get('comfirmpassword')
		if password != comfirm_password:
			messages.error(request, "Mot de passe non identique")
			return self.get(self, request, *args, **kwargs)

		user = self.user
		profile = user.profile

		user.set_password(password)
		profile.token_forget_password = None

		with transaction.atomic():
			user.save()
			profile.save()

		messages.success(request, "Mot de passe changé")
		return redirect("core:login")


@no_tenant_required
def register(request: HttpRequest) -> HttpResponse:
	print("started")
	data = {
		'titre': "pade d'accueil",
		# 'cats': models.Categorie.objects.filter(status=True)
	}
	print("ended")
	return render(request, 'pages/register.html', data)


def add_tenant_user(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		name = request.POST.get('name')
		unique_domain = request.POST.get('unique_domain')
		lastname = request.POST.get('lastname')
		firstname = request.POST.get('firstname')
		username = request.POST.get('username')
		email = request.POST.get('email')
		contact = request.POST.get('tel')
		password = request.POST.get('formValidationPass')
		# TODO: Valider les donner avant de continuer
		add_tenant = tenant_models.Tenant(
			name=name,
			unique_domain=unique_domain
		)
		u = fleet_models.User(
			first_name=firstname,
			last_name=lastname,
			username=username,
			email=email,
			password=password
		)
		fleet_user = fleet_models.FleetUser(
			user=u,
			tenant=add_tenant,
			contact=contact,
		)
		with transaction.atomic():
			add_tenant.save()
			u.set_password(u.password)
			u.save()
			fleet_user.save()
		return redirect("core:tenant:home", tenant=add_tenant.unique_domain)
	else:
		return redirect("core:home")


@no_tenant_required
def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(
				username=form.cleaned_data["username"],
				password=form.cleaned_data["password"]
			)
			if user is not None and hasattr(user, 'profile'):
				auth_login(request, user)
				print('CO : ', user.profile.is_new)
				if user.profile.is_new:
					print('CO1 : ', user.profile.is_new)
					return redirect('core:change_password')
				else:
					tenant = user.profile.tenant
					return redirect('core:tenant:home', tenant=tenant.unique_domain)
	data = {
		'titre': "page de connexion",
		# 'cats': models.Categorie.objects.filter(status=True)
	}
	return render(request, 'pages/login.html', data)


def add_contact(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		full_name = request.POST.get('full_name')
		email = request.POST.get('email')
		message = request.POST.get('message')
		contact = core_models.Contact(
			full_name=full_name,
			email=email,
			message=message,
		)
		contact.save()
		#subject = 'Contactez-nous sur Fleet-Wise'
		#email_from = settings.EMAIL_HOST_USER
		#message = message
		#recipient_list = [email]
		#send_mail(subject, message, email_from, recipient_list, fail_silently=False)
		messages.success(request, "Formulaire envoyé")
		return redirect('core:home')
	else:
		messages.error(request, "Formulaire non envoyé")
		return redirect("core:home")


def add_newsletter(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		full_name = request.POST.get('full_name')
		email = request.POST.get('email')
		entreprise = request.POST.get('entreprise')
		newsletter = core_models.Newsletter(
			full_name=full_name,
			email=email,
			entreprise=entreprise,
		)
		newsletter.save()
		messages.success(request, "Newsletter envoyé")
		return redirect('core:home')
	else:
		messages.error(request, "Newsletter non envoyé")
		return redirect("core:home")


def validate_domain(request):
	unique_domain = request.POST.get('unique_domain', None)
	data = {
		'is_taken': tenant_models.Tenant.objects.filter(unique_domain=unique_domain).exists()
	}
	return JsonResponse(data)


def change_password(request: HttpRequest) -> HttpResponse:
	data = {
	}
	print("ended")
	return render(request, 'pages/update_password.html', data)


def change_password_user(request: HttpRequest) -> HttpResponse:
	if request.method != "POST":
		return redirect("core:home")
	password = request.POST.get('password')
	comfirm_password = request.POST.get('comfirmpassword')
	if password != comfirm_password:
		messages.error(request, "Mot de passe non identique")
		return redirect("core:home")

	user = request.user
	tenant = user.profile.tenant
	profile = user.profile

	user.set_password(password)
	profile.is_new = False
	user.save()
	profile.save()
	print("Update :", user.profile.is_new)
	auth_logout(request)
	return redirect("core:login")


def logout(request):
	auth_logout(request)
	return redirect('core:home')
