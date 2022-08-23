from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import CommentForm, EntryForm, TapeForm
from .models import Bookmark, Entry, Like, Subscribe, Tape, User
from .utils import htmx_login_required, pagination


class EntriesListView(ListView):
    model = Entry
    template_name = 'entries/index.html'
    context_object_name = 'entries'
    paginate_by = settings.ENTRIES_COUNT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.htmx:
            self.template_name = 'includes/entry_list.html'
        return context


class FeedView(LoginRequiredMixin, EntriesListView):
    template_name = 'entries/feed.html'

    def get_queryset(self):
        user = self.request.user
        return Entry.objects.filter(author__subs__user=user)


class SavedView(LoginRequiredMixin, EntriesListView):
    template_name = 'entries/saved.html'

    def get_queryset(self):
        user = self.request.user
        return Entry.objects.filter(marked__user=user)


class LikedView(LoginRequiredMixin, EntriesListView):
    template_name = 'entries/liked.html'

    def get_queryset(self):
        user = self.request.user
        return Entry.objects.filter(liked__user=user)


class TapeView(EntriesListView):
    template_name = 'entries/tape.html'

    def get_queryset(self):
        username = self.kwargs['username']
        slug = self.kwargs['slug']
        author = get_object_or_404(User, username=username)
        tapes = get_object_or_404(Tape, slug=slug, author=author)
        return tapes.entries.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        slug = self.kwargs['slug']
        author = get_object_or_404(User, username=username)
        tapes = get_object_or_404(Tape, slug=slug, author=author)
        extra_context = {
            'tapes': tapes,
            'author': author,
        }
        context.update(extra_context)
        return context


class TapeAddView(LoginRequiredMixin, CreateView):
    form_class = TapeForm
    template_name = 'entries/tape_add.html'
    # add get_success_url method


class TapeUpdateView(LoginRequiredMixin, UpdateView):
    model = Tape
    form_class = TapeForm
    template_name = 'entries/tape_add.html'
    extra_context = {'is_edit': True}

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs['username'] != self.request.user.username:
            return HttpResponseForbidden()
        return super(TapeUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        username = self.kwargs['username']
        slug = self.kwargs['slug']
        success_url = reverse_lazy('entries:tape', kwargs={
                                   'username': username, 'slug': slug})
        return success_url


class EntryDetailView(DetailView):
    model = Entry
    template_name = 'entries/entry_detail.html'
    pk_field = 'entry_id'
    pk_url_kwarg = 'entry_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.object
        form = CommentForm()
        comments = entry.comments.all()
        comments = pagination(self.request, comments, settings.COMMENTS_COUNT)
        extra_context = {
            'form': form,
            'comments': comments,
        }
        context.update(extra_context)
        return context


class EntryAddView(LoginRequiredMixin, CreateView):
    form_class = EntryForm
    template_name = 'entries/entry_add.html'
    # add get_success_url method

    def get_form_kwargs(self):
        kwargs = super(EntryAddView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entries/entry_add.html'
    extra_context = {'is_edit': True}
    pk_field = 'entry_id'
    pk_url_kwarg = 'entry_id'

    def get_form_kwargs(self):
        kwargs = super(EntryUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return HttpResponseForbidden()
        return super(EntryUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        entry_id = self.kwargs['entry_id']
        success_url = reverse_lazy('entries:entry_detail', kwargs={
                                   'entry_id': entry_id})
        return success_url


class CommentAddView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = 'entries/entry_add.html'
    pk_field = 'entry_id'
    pk_url_kwarg = 'entry_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.entry = get_object_or_404(
            Entry, id=self.kwargs['entry_id'])
        return super().form_valid(form)

    def get_success_url(self):
        entry_id = self.kwargs['entry_id']
        success_url = reverse_lazy('entries:entry_detail', kwargs={
                                   'entry_id': entry_id})
        return success_url


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
    return redirect('users:profile', username)


@login_required
def unsubscribe(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    Subscribe.objects.filter(user=user, author=author).delete()
    return redirect('users:profile', username)
