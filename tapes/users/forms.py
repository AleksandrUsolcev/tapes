from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from client_side_image_cropping import ClientsideCroppingWidget

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'show_full_name', 'about', 'avatar')
        widgets = {
            'avatar': ClientsideCroppingWidget(
                width=300,
                height=300,
                preview_width=150,
                preview_height=150,
            )
        }
