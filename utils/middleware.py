from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


class EnsureCSRFMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        return method_decorator(ensure_csrf_cookie)(view_func)(request, *view_args, **view_kwargs)
