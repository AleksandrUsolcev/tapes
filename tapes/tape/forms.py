from django import forms

from tape.models import Comment, Entry, Tape


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('text', 'tape')
        labels = {'text': 'Ваш текст', 'tape': 'Сообщества'}
        help_texts = {
            'text': '*данное поле обязательно для заполнения',
            'tape': 'к какому сообществу будет отнесён пост',
        }


class TapeForm(forms.ModelForm):
    class Meta:
        model = Tape
        fields = ('title', 'slug', 'description')
