from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings

from tape.forms import CommentForm
from tape.models import Entry, Like, Bookmark, User, Comment
from tape.utils import pagination


def index(request):
    entries = Entry.objects.all()
    entries = pagination(request, entries, settings.ENTRIES_COUNT)
    context = {
        'entries': entries,
    }
    return render(request, 'tape/index.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    entries = Entry.objects.filter(author=user)
    entries = pagination(request, entries, settings.ENTRIES_COUNT)
    context = {
        'user': user,
        'entries': entries,
    }
    return render(request, 'tape/profile.html', context)


def tape(request):
    pass


@login_required
def tape_add(request):
    pass


@login_required
def feed(request):
    pass


def entry_detail(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    form = CommentForm()
    comments = entry.comments.all()
    comments = pagination(request, comments, settings.COMMENTS_COUNT)
    context = {
        'entry': entry,
        'form': form,
        'comments': comments,
    }
    return render(request, 'tape/entry_detail.html', context)


@login_required
def entry_add(request):
    pass


@login_required
def comment_add(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.entry = entry
        form.save()
        return redirect('tape:entry_detail', entry_id=entry_id)
    context = {
        'entry': entry,
        'form': form
    }
    return render(request, 'tape/entry_detail.html', context)


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
