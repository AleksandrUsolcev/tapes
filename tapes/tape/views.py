from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from talks.forms import TalkForm
from tape.forms import EntryForm, TapeAddForm, TapeEditForm
from tape.models import Entry, Like, Bookmark, User, Subscribe, Tape
from tape.utils import pagination, htmx_login_required


def index(request):
    entries = Entry.objects.all()
    entries = pagination(request, entries, settings.ENTRIES_COUNT)
    context = {
        'entries': entries,
    }
    if request.user.is_authenticated and request.user.is_newbie:
        request.user.is_newbie = False
        request.user.save()
    if request.htmx:
        return render(request, 'includes/entry_list.html', context)
    return render(request, 'tape/index.html', context)


def profile(request, username):
    username.lower()
    user = get_object_or_404(User, username=username)
    entries = Entry.objects.filter(author=user)
    entries = pagination(request, entries, settings.ENTRIES_COUNT)
    author = get_object_or_404(User, username=username)
    tapes = Tape.objects.filter(author=user)
    if request.user.is_authenticated:
        is_sub = Subscribe.objects.filter(
            user=request.user,
            author=author
        ).exists()
    else:
        is_sub = False
    if request.user.is_authenticated:
        form = EntryForm(request.POST or None,
                         files=request.FILES or None,
                         user_id=request.user
                         )
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('tape:profile', username=request.user.username)
    else:
        form = False
    context = {
        'user': user,
        'author': author,
        'entries': entries,
        'is_sub': is_sub,
        'tapes': tapes,
        'form': form,
    }
    if request.htmx:
        return render(request, 'includes/entry_list.html', context)
    return render(request, 'tape/profile.html', context)


def tape(request, username, slug):
    username.lower()
    slug.lower()
    author = get_object_or_404(User, username=username)
    tapes = get_object_or_404(Tape, slug=slug, author=author)
    entries = tapes.entries.all()
    entries = pagination(request, entries, settings.ENTRIES_COUNT)
    context = {
        'entries': entries,
        'tapes': tapes,
        'author': author,
    }
    if request.htmx:
        return render(request, 'includes/entry_list.html', context)
    return render(request, 'tape/tape.html', context)


@login_required
def tape_add(request):
    form = TapeAddForm(request.POST or None, files=request.FILES or None, )
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect(
            'tape:tape',
            username=request.user.username,
            slug=form.slug,
        )
    return render(request, 'tape/tape_add.html', {'form': form})


@login_required
def tape_edit(request, username, slug):
    username.lower()
    user = request.user
    tapes = get_object_or_404(Tape, slug=slug, author=user)
    author = tapes.author
    form = TapeEditForm(
        request.POST or None,
        files=request.FILES or None,
        instance=tapes,
    )
    if author != request.user:
        return redirect('tape:tape', slug=slug, username=tapes.author.username)
    if form.is_valid():
        if author == request.user and form.cleaned_data["delete_tape"] is True:
            tapes.delete()
            return redirect('tape:profile', username=tapes.author.username)
        form.save()
        return redirect('tape:tape', slug=slug, username=tapes.author.username)
    context = {
        'is_edit': True,
        'form': form
    }
    return render(request, 'tape/tape_add.html', context)


@login_required
def feed(request):
    user = request.user
    entries = Entry.objects.filter(author__subs__user=user)
    entries = pagination(request, entries, settings.ENTRIES_COUNT)
    context = {
        'entries': entries,
    }
    if request.htmx:
        return render(request, 'includes/entry_list.html', context)
    return render(request, 'tape/feed.html', context)


@login_required
def saved(request):
    user = request.user
    entries = Entry.objects.filter(marked__user=user)
    entries = pagination(request, entries, settings.ENTRIES_COUNT)
    context = {
        'entries': entries,
    }
    if request.htmx:
        return render(request, 'includes/entry_list.html', context)
    return render(request, 'tape/saved.html', context)


@login_required
def liked(request):
    user = request.user
    entries = Entry.objects.filter(liked__user=user)
    entries = pagination(request, entries, settings.ENTRIES_COUNT)
    context = {
        'entries': entries,
    }
    if request.htmx:
        return render(request, 'includes/entry_list.html', context)
    return render(request, 'tape/liked.html', context)


def entry_detail(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    form = TalkForm()
    talks = entry.talks.all()
    talks = pagination(request, talks, settings.TALKS_COUNT)
    context = {
        'entry': entry,
        'form': form,
        'talks': talks,
    }
    if request.htmx:
        return render(request, 'talks/list.html', context)
    return render(request, 'tape/entry_detail.html', context)


@login_required
def entry_add(request):
    form = EntryForm(request.POST or None,
                     files=request.FILES or None,
                     user_id=request.user
                     )
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect('tape:profile', username=request.user.username)
    return render(request, 'tape/entry_add.html', {'form': form})


@login_required
def entry_edit(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    form = EntryForm(request.POST or None,
                     files=request.FILES or None,
                     user_id=request.user,
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


@htmx_login_required
def like_entry(request, entry_id):
    if request.method == 'POST':
        user = request.user
        entry = get_object_or_404(Entry, id=entry_id)
        instance = Like.objects.filter(user=user, entry=entry)
        if not instance:
            Like.objects.get_or_create(user=user, entry=entry)
        else:
            Like.objects.filter(user=user, entry=entry).delete()
        return render(request, 'htmx/like-area.html',
                      context={'entry': entry})


@htmx_login_required
def mark_entry(request, entry_id):
    user = request.user
    entry = get_object_or_404(Entry, id=entry_id)
    instance = Bookmark.objects.filter(user=user, entry=entry)
    if not instance:
        Bookmark.objects.get_or_create(user=user, entry=entry)
    else:
        Bookmark.objects.filter(user=user, entry=entry).delete()
    return render(request, 'htmx/mark-area.html',
                  context={'entry': entry})


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
