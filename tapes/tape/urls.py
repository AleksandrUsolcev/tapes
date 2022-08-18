from django.urls import path

from . import views

app_name = 'tape'

urlpatterns = [
    path('', views.index, name='index'),
    path('~<str:username>', views.profile, name='profile'),
    path('feed', views.feed, name='feed'),
    path('new-tape', views.tape_add, name='tape_add'),
    path('new', views.entry_add, name='entry_add'),
    path('saved', views.saved, name='saved'),
    path('liked', views.liked, name='liked'),
    path(
        'entries/<int:entry_id>',
        views.entry_detail,
        name='entry_detail'
    ),
    path('entries/<int:entry_id>/edit', views.entry_edit, name='entry_edit'),
    path(
        'entries/<int:entry_id>/comment',
        views.comment_add,
        name='comment_add'
    ),
    path(
        'entries/<int:entry_id>/like_entry',
        views.like_entry,
        name='like_entry'
    ),
    path(
        'entries/<int:entry_id>/mark_entry',
        views.mark_entry,
        name='mark_entry'
    ),
    path(
        '~<str:username>/subscribe',
        views.subscribe,
        name='subscribe'
    ),
    path(
        '~<str:username>/unsubscribe',
        views.unsubscribe,
        name='unsubscribe'
    ),
    path('~<str:username>/<slug:slug>', views.tape, name='tape'),
    path('~<str:username>/<slug:slug>/edit',
         views.tape_edit,
         name='tape_edit'
         ),
]
