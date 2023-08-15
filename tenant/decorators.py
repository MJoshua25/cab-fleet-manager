from functools import wraps
from django.shortcuts import redirect

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
	from tenant.models import Tenant


def no_tenant_required(view_func):
	@wraps(view_func)
	def _wrapped_view(request, *args, **kwargs):
		if request.user.is_authenticated:
			tenant: Tenant = request.user.profile.tenant
			# L'utilisateur est connecté, redirigez vers l'URL 'core:tenant:home'
			return redirect('core:tenant:home', tenant=tenant.unique_domain)
		else:
			# L'utilisateur n'est pas connecté, laissez-le accéder à la page
			return view_func(request, *args, **kwargs)

	return _wrapped_view
