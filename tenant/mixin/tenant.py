from django.shortcuts import render, redirect
from django.views.generic.base import ContextMixin
from django.apps import apps

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
	from tenant.models import Tenant


class TenantAwareViewMixin(ContextMixin):
	tenant: 'Union[Tenant, None]' = None

	def dispatch(self, request, *args, **kwargs):
		# Vérifier si l'utilisateur est connecté
		print(request.user, self.request.user, request.user.is_authenticated)
		if not request.user.is_authenticated:
			return redirect('core:login')

		# Récupérer le paramètre 'tenant' de l'URL
		tenant = kwargs.get('tenant', None)
		if not tenant:
			return redirect('core:home')

		self.tenant: 'Tenant' = apps.get_model('tenant', 'Tenant').objects.filter(unique_domain=tenant).first()
		print(self.request.user.username)

		# Vérifier si le tenant existe, sinon rediriger vers une autre vue
		if not self.tenant:
			return redirect('core:home')

		# Vérifier si l'utilisateur a le même tenant que celui spécifié dans l'URL
		if self.tenant.unique_domain != self.request.user.profile.tenant.unique_domain:
			return redirect('core:home')

		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Ajouter les données que vous souhaitez au contexte ici
		context['unique_domain'] = self.tenant.unique_domain
		print(self.tenant.unique_domain)
		return context
