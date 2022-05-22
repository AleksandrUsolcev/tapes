from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from tape.models import Entry, Like, Bookmark
from tape.utils import pagination


def index(request):
    entries = Entry.objects.all()
    entries = pagination(request, entries)
    context = {
        'entries': entries,
    }
    return render(request, 'tape/index.html', context)


def profile(request):
    pass


def tape(request):
    pass


@login_required
def tape_add(request):
    pass


@login_required
def feed(request):
    pass


def entry_detail(request):
    pass


@login_required
def entry_add(request):
    pass


@login_required
def comment_add(request):
    pass


@login_required
def like_add(request, entry_id):
    user = request.user
    entry = get_object_or_404(Entry, id=entry_id)
    Like.objects.get_or_create(user=user, entry=entry)
    return redirect('tape:index')


@login_required
def dislike(request, entry_id):
    user = request.user
    entry = get_object_or_404(Entry, id=entry_id)
    Like.objects.filter(user=user, entry=entry).delete()
    return redirect('tape:index')


@login_required
def mark_add(request, entry_id):
    user = request.user
    entry = get_object_or_404(Entry, id=entry_id)
    Bookmark.objects.get_or_create(user=user, entry=entry)
    return redirect('tape:index')


@login_required
def unmark(request, entry_id):
    user = request.user
    entry = get_object_or_404(Entry, id=entry_id)
    Bookmark.objects.filter(user=user, entry=entry).delete()
    return redirect('tape:index')
