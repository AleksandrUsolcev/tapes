from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from tape.forms import CommentForm, EntryForm, TapeForm
from tape.models import Entry, Like, Bookmark, User, Subscribe, Tape
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
    author = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        is_sub = Subscribe.objects.filter(
            user=request.user,
            author=author
        ).exists()
    else:
        is_sub = False
    context = {
        'user': user,
        'author': author,
        'entries': entries,
        'is_sub': is_sub,
    }
    return render(request, 'tape/profile.html', context)


def tape(request, username, slug):
    author = get_object_or_404(User, username=username)
    tapes = get_object_or_404(Tape, slug=slug, author=author)
    entries = tapes.entries.all()
    entries = pagination(request, entries, settings.ENTRIES_COUNT)
    context = {
        'entries': entries,
    }
    return render(request, 'tape/feed.html', context)


@login_required
def tape_add(request):
    form = TapeForm(request.POST or None, files=request.FILES or None, )
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect('tape:profile', username=request.user.username)
    return render(request, 'tape/tape_add.html', {'form': form})


@login_required
def feed(request):
    user = request.user
    entries = Entry.objects.filter(author__subs__user=user)
    entries = pagination(request, entries, settings.ENTRIES_COUNT)
    context = {
        'entries': entries,
    }
    return render(request, 'tape/feed.html', context)


@login_required
def saved(request):
    user = request.user
    entries = Entry.objects.filter(marked__user=user)
    entries = pagination(request, entries, settings.ENTRIES_COUNT)
    context = {
        'entries': entries,
    }
    return render(request, 'tape/saved.html', context)


@login_required
def liked(request):
    user = request.user
    entries = Entry.objects.filter(liked__user=user)
    entries = pagination(request, entries, settings.ENTRIES_COUNT)
    context = {
        'entries': entries,
    }
    return render(request, 'tape/liked.html', context)


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
    form = EntryForm(request.POST or None, files=request.FILES or None, )
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect('tape:profile', username=request.user.username)
    return render(request, 'tape/entry_add.html', {'form': form})


@login_required
def entry_edit(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    form = EntryForm(
        request.POST or None,
        files=request.FILES or None,
        instance=entry
    )
    if entry.author != request.user:
        return redirect('tape:entry_detail', entry_id=entry_id)
    if form.is_valid():
        form.save()
        return redirect('tape:entry_detail', entry_id=entry_id)
    context = {
        'is_edit': True,
        'entry': entry,
        'form': form,
    }
    return render(request, 'tape/entry_add.html', context)


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


@login_required
def subscribe(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    if user != author:
        Subscribe.objects.get_or_create(user=user, author=author)
    return redirect('tape:profile', username)


@login_required
def unsubscribe(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    Subscribe.objects.filter(user=user, author=author).delete()
    return redirect('tape:profile', username)
