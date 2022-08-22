from bootstrap_modal_forms.generic import BSModalCreateView, BSModalLoginView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from entries.forms import EntryForm
from entries.models import Entry, Subscribe, Tape

from .forms import (CustomAuthenticationForm, CustomUserCreationForm,
                    UserEditForm)
from .models import User
from .utils import pagination


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup_modal.html'
    success_message = 'Вы успешно зарегистрировались'

    def get_success_url(self):
        success_url = reverse_lazy('users:user_edit')
        return success_url


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login_modal.html'
    success_message = 'Вы успешно вошли в учетную запись'
    extra_context = dict(success_url=reverse_lazy('entries:index'))


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
            return redirect('users:profile', username=request.user.username)
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
    return render(request, 'users/profile.html', context)


@login_required
def user_edit(request):
    user = request.user
    form = UserEditForm(
        request.POST or None,
        files=request.FILES or None,
        instance=request.user
    )
    if form.is_valid():
        form.save()
        return redirect('users:profile', username=request.user.username)
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'users/profile_edit.html', context)
