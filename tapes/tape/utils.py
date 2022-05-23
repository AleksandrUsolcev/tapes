from django.core.paginator import Paginator


def pagination(request, entries, count):
    page_number = request.GET.get('page')
    paginator = Paginator(entries, count)
    return paginator.get_page(page_number)
