from bootstrap_modal_forms.generic import BSModalLoginView, BSModalCreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, UserEditForm, \
    CustomAuthenticationForm


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup_modal.html'
    success_message = 'Вы успешно зарегистрировались'

    def get_success_url(self):
        success_url = reverse_lazy('users:user_edit')
        return success_url


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
    template_name = 'users/login-modal.html'
    success_message = 'Вы успешно вошли в учетную запись'
    extra_context = dict(success_url=reverse_lazy('tape:index'))
