from client_side_image_cropping import ClientsideCroppingWidget
from django import forms

from .models import Comment, Entry, Tape


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('text', 'title', 'tape')

    tape = forms.ModelChoiceField(label='', queryset=Tape.objects.none())

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['tape'].queryset = Tape.objects.filter(author=user_id)


class TapeAddForm(forms.ModelForm):
    class Meta:
        model = Tape
        fields = ('title', 'slug', 'description', 'background')
        widgets = {
            'background': ClientsideCroppingWidget(
                width=1000,
                height=300,
                preview_width=1000,
                preview_height=300,
            )
        }


class TapeEditForm(forms.ModelForm):
    delete_tape = forms.BooleanField(label='Удалить ленту', required=False)

    class Meta:
        model = Tape
        fields = ('description', 'background', 'slug', 'title')
        widgets = {
            'background': ClientsideCroppingWidget(
                width=1000,
                height=300,
                preview_width=1000,
                preview_height=300,
            )
        }