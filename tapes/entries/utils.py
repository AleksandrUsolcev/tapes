from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import \
    login_required as django_login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import resolve_url


def htmx_login_required(function=None, login_url=None,
                        redirect_field_name=REDIRECT_FIELD_NAME):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated and request.htmx:
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            return HttpResponse(status=204,
                                headers={'HX-Redirect': resolved_login_url})
        return django_login_required(
            function=function,
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )(request, *args, **kwargs)
    return wrapper


def pagination(request, entries, count):
    page_number = request.GET.get('page')
    paginator = Paginator(entries, count)
    return paginator.get_page(page_number)
