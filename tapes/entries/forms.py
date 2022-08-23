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
        user = kwargs.pop('user', None)
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['tape'].queryset = Tape.objects.filter(author=user)


class TapeForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.is_add = kwargs.pop('is_add', None)
        super(TapeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        slug = self.cleaned_data['slug'].lower()
        created = Tape.objects.filter(author=self.user, slug=slug).exists()
        if self.is_add and created:
            raise forms.ValidationError('У вас уже есть лента с указанной'
                                        ' ссылкой')
        return cleaned_data
