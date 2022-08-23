from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_quill.fields import QuillField

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=255,
        unique=True,
    )
    username = models.SlugField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=24,
        blank=False,
        null=False,
    )
    username_lower = models.SlugField(
        verbose_name='Уникальное имя',
        unique=True,
        max_length=24,
        blank=False,
        null=False,
    )
    about = QuillField(
        verbose_name='Краткое описание',
        blank=True,
        null=True
    )
    full_name = models.CharField(
        verbose_name='Полное имя',
        max_length=48,
        blank=True,
        null=True
    )
    show_full_name = models.BooleanField(
        verbose_name='Отображать полное имя',
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name='Администрация',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=True
    )
    is_verified = models.BooleanField(
        verbose_name='Аккаунт подтвержден',
        default=False
    )
    is_newbie = models.BooleanField(
        verbose_name='Только что зарегистрирован',
        default=True
    )
    date_joined = models.DateTimeField(
        verbose_name='Дата регистрации',
        default=timezone.now
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='user-avatars/',
        blank=True
    )
    background = models.ImageField(
        verbose_name='Фон профиля',
        upload_to='user-backgrounds/',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username_lower = self.username.lower()
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})
