from django.contrib.auth import get_user_model
from django.db import models

from tape.models import Entry

User = get_user_model()


class Talk(models.Model):
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name='talks'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='talks'
    )
    text = models.TextField()
    reply = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.text[:30]
