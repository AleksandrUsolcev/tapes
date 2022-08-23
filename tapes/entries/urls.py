from django.urls import path

from . import views

app_name = 'entries'

urlpatterns = [
    path('', views.EntriesListView.as_view(), name='index'),
    path('feed', views.FeedView.as_view(), name='feed'),
    path('new', views.EntryAddView.as_view(), name='entry_add'),
    path('saved', views.SavedView.as_view(), name='saved'),
    path('liked', views.LikedView.as_view(), name='liked'),
    path(
        'entries/<int:entry_id>',
        views.EntryDetailView.as_view(),
        name='entry_detail'
    ),
    path('entries/<int:entry_id>/edit',
         views.EntryUpdateView.as_view(),
         name='entry_edit'
         ),
    path(
        'entries/<int:entry_id>/comment',
        views.CommentAddView.as_view(),
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
        '~<slug:username>/subscribe',
        views.subscribe,
        name='subscribe'
    ),
    path(
        '~<slug:username>/unsubscribe',
        views.unsubscribe,
        name='unsubscribe'
    ),
    path('~<slug:username>/<slug:slug>',
         views.TapeView.as_view(),
         name='tape'),
    path('new-tape', views.TapeAddView.as_view(), name='tape_add'),
    path('~<slug:username>/<slug:slug>/edit',
         views.TapeUpdateView.as_view(),
         name='tape_edit'
         ),
]
