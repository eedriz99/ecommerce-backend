from django.contrib.auth.decorators import login_required
from functools import wraps


def login_required_for_non_get(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method != 'GET':
            return login_required(view_func, login_url='/login/')(request, *args, **kwargs)
        return view_func(request, *args, **kwargs)
    return wrapper
