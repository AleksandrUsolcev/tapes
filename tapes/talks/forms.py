from django import forms

from .models import Talk


class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('text',)
