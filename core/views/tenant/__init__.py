from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from tenant.mixin import TenantAwareViewMixin


class IndexView(TenantAwareViewMixin, TemplateView):
	template_name = 'pages/tenant/index.html'
