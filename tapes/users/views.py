from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm, UserEditForm


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('tape:index')
    template_name = 'users/signup.html'


@login_required
def user_edit(request):
    about = request.user.about
    form = UserEditForm(
        request.POST or None,
        instance=about
    )
    if form.is_valid():
        form.save()
        return redirect('tape:profile')
    context = {
        'form': form
    }
    return render(request, 'users/profile_edit.html', context)
