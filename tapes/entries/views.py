from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import (CreateView, DetailView, ListView, UpdateView,
                                  View)

from .forms import CommentForm, EntryForm, TapeForm
from .mixins import UserOwnershipMixin
from .models import Bookmark, Entry, Like, Tape, User
from .utils import pagination


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
        return Entry.objects.filter(author__subs__user=self.request.user)


class SavedView(LoginRequiredMixin, EntriesListView):
    template_name = 'entries/saved.html'

    def get_queryset(self):
        return Entry.objects.filter(marked__user=self.request.user)


class LikedView(LoginRequiredMixin, EntriesListView):
    template_name = 'entries/liked.html'

    def get_queryset(self):
        return Entry.objects.filter(liked__user=self.request.user)


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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TapeUpdateView(LoginRequiredMixin, UserOwnershipMixin, UpdateView):
    model = Tape
    form_class = TapeForm
    template_name = 'entries/tape_add.html'
    extra_context = {'is_edit': True}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EntryDetailView(DetailView):
    model = Entry
    template_name = 'entries/entry_detail.html'
    pk_field = 'entry_id'
    pk_url_kwarg = 'entry_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comments = self.object.comments.all()
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

    def get_form_kwargs(self):
        kwargs = super(EntryAddView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EntryUpdateView(LoginRequiredMixin, UserOwnershipMixin, UpdateView):
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


class LikeEntryView(LoginRequiredMixin, View):
    model = Like
    template_name = 'htmx/like-area.html'

    def post(self, request, **kwargs):
        user = request.user
        entry_id = self.kwargs['entry_id']
        entry = get_object_or_404(Entry, id=entry_id)
        instance = self.model.objects.filter(user=user, entry=entry)
        if not instance:
            self.model.objects.get_or_create(user=user, entry=entry)
        else:
            self.model.objects.filter(user=user, entry=entry).delete()
        return render(request, self.template_name, context={'entry': entry})


class MarkEntryView(LikeEntryView):
    model = Bookmark
    template_name = 'htmx/mark-area.html'
