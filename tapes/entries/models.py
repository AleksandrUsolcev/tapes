from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_quill.fields import QuillField

User = get_user_model()


class Tape(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tapes'
    )
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, verbose_name='Название ленты')
    slug = models.SlugField(
        unique=False,
        max_length=32,
        verbose_name='Ссылка'
    )
    description = QuillField(
        blank=True,
        null=True,
        max_length=400,
        verbose_name='Описание'
    )
    background = models.ImageField(upload_to='tape-backgrounds/', blank=True)

    class Meta:
        unique_together = ('author', 'slug',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.slug.lower()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        username = self.author.username
        slug = self.slug
        return reverse(
            'entries:tape', kwargs={'username': username, 'slug': slug})


class Entry(models.Model):
    title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Заголовок',
    )
    text = QuillField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='entries'
    )
    tape = models.ForeignKey(
        Tape,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='entries',
        verbose_name='Лента'
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.text.plain[:30]

    def get_absolute_url(self):
        return reverse(
            'entries:entry_detail', kwargs={'entry_id': self.id})


class Comment(models.Model):
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = QuillField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse(
            'entries:entry_detail', kwargs={'entry_id': self.entry.id})


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='like'
    )
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name='liked'
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'entry'],
                name='unique_like',
            )
        ]

    def __str__(self):
        return f'{self.user.username} like {self.entry.pk}'


class Bookmark(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mark'
    )
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name='marked'
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'entry'],
                name='unique_bookmark',
            )
        ]
