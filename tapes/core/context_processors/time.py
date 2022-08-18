from django.utils import timezone


def today_time(request):
    return {
        'today_time': timezone.now().date(),
    }
