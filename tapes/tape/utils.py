from django.conf import settings
from django.core.paginator import Paginator


def pagination(request, entries):
    page_number = request.GET.get('page')
    paginator = Paginator(entries, settings.ENTRIES_COUNT)
    return paginator.get_page(page_number)
