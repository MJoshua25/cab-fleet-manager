from django.http import HttpResponseRedirect, HttpRequest, HttpResponse, JsonResponse


def get_current_host(request: HttpRequest) -> str:
	scheme = request.is_secure() and "https" or "http"
	return f'{scheme}://{request.get_host()}'
