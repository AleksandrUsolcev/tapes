from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tape(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tapes'
    )
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, verbose_name='Название ленты')
    slug = models.SlugField(max_length=48, verbose_name='Ссылка')
    description = models.TextField(
        blank=True,
        null=True,
        max_length=400,
        verbose_name='Описание'
    )

    def __str__(self):
        return self.title


class Entry(models.Model):
    title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Заголовок',
    )
    text = models.TextField(verbose_name='Текст')
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
        return self.text[:30]


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
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.text[:30]


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sub'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subs'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe',
            )
        ]


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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'entry'],
                name='unique_like',
            )
        ]


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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'entry'],
                name='unique_bookmark',
            )
        ]
