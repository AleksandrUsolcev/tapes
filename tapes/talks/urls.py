from django.urls import path

from . import views

app_name = 'talks'

urlpatterns = [
    path(
        '<int:entry_id>/talk',
        views.talk_add,
        name='talk_add'
    ),
    path(
        'talks/<int:talk_id>/detail',
        views.talk_detail,
        name='talk_detail'
    ),
    path(
        '<int:entry_id>/talk/<int:talk_id>/reply',
        views.talk_reply,
        name='talk_reply'
    ),
]
