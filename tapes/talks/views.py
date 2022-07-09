from .models import Talk
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TalkForm
from tape.models import Entry
from tape.utils import pagination


def talk_detail(request, talk_id):
    talk = get_object_or_404(Talk, id=talk_id)
    form = TalkForm()
    replies = talk.replies.all()
    replies = pagination(
        request, replies,
        settings.TALKS_COUNT
    )
    context = {
        'talk': talk,
        'form': form,
        'replies': replies
    }
    if request.htmx:
        return render(request, 'talks/detail_list.html', context)
    return render(request, 'talks/detail.html', context)


@login_required
def talk_add(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    form = TalkForm(request.POST or None)
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
def talk_reply(request, entry_id, talk_id):
    entry = get_object_or_404(Entry, id=entry_id)
    talk = get_object_or_404(Talk, id=talk_id)
    form = TalkForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.entry = entry
        form.reply = talk
        form.save()
        return redirect('tape:entry_detail', entry_id=entry_id)
    context = {
        'entry': entry,
        'form': form,
        'talk': talk
    }
    return render(request, 'talks/reply_form.html', context)
