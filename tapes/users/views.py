from bootstrap_modal_forms.generic import BSModalLoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from tape.models import User
from .forms import CustomUserCreationForm, UserEditForm, \
    CustomAuthenticationForm


def user_create(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        form.save()
        new_user = User.objects.get(username=username.lower())
        if new_user:
            new_user.display_username = username
            new_user.save()
        return redirect('tape:index')
    context = {
        'form': form
    }
    return render(request, 'users/signup.html', context)


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
        return redirect('tape:profile', username=request.user.username)
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'users/profile_edit.html', context)


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_message = 'Success: You were successfully logged in.'
    extra_context = dict(success_url=reverse_lazy('tape:index'))
