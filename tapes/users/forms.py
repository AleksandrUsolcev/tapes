from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from client_side_image_cropping import ClientsideCroppingWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    AuthenticationForm

from .models import CustomUser


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin,
                             UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'display_username')
        widgets = {'display_username': forms.HiddenInput()}


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'show_full_name', 'about', 'avatar',
                  'background')
        labels = {
            'full_name': 'Имя или название организации',
            'show_full_name': 'Отображать имя в постах',
            'about': 'Обо мне'
        }
        widgets = {
            'avatar': ClientsideCroppingWidget(
                width=300,
                height=300,
                preview_width=150,
                preview_height=150,
            ),
            'background': ClientsideCroppingWidget(
                width=1000,
                height=300,
                preview_width=1000,
                preview_height=300,
            )
        }
