from bootstrap_modal_forms.generic import BSModalCreateView, BSModalLoginView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, View
from entries.models import Entry

from .forms import (CustomAuthenticationForm, CustomUserCreationForm,
                    UserEditForm)
from .models import Subscribe, User
from .utils import pagination


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup_modal.html'

    def get_success_url(self):
        success_url = reverse_lazy('entries:index')
        return success_url


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login_modal.html'


class UserProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        entries = Entry.objects.filter(author=author)
        entries = pagination(self.request, entries, settings.ENTRIES_COUNT)
        if self.request.user.is_authenticated:
            is_sub = Subscribe.objects.filter(
                user=self.request.user,
                author=author
            ).exists()
        else:
            is_sub = False
        extra_context = {
            'entries': entries,
            'is_sub': is_sub,
        }
        context.update(extra_context)
        if self.request.htmx:
            self.template_name = 'includes/entry_list.html'
        return context


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'users/profile_edit.html'

    def get_object(self, queryset=None):
        return self.model.objects.get(username=self.request.user.username)


class SubscribeView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        user = request.user
        username = self.kwargs['username']
        author = get_object_or_404(User, username=username)
        instance = Subscribe.objects.filter(user=user, author=author)
        if user != author:
            if not instance:
                Subscribe.objects.get_or_create(user=user, author=author)
            else:
                Subscribe.objects.filter(user=user, author=author).delete()
        return redirect('users:profile', username)
