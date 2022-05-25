from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .fields import LowercaseEmailField, LowercaseCharField
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = LowercaseEmailField(_('email address'), unique=True)
    username = LowercaseCharField(
        unique=True,
        max_length=24,
        blank=False,
        null=False
    )
    about = models.TextField(max_length=200, blank=True, null=True)
    display_username = models.CharField(max_length=24, blank=True, null=True)
    full_name = models.CharField(max_length=48, blank=True, null=True)
    show_full_name = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='user-avatars/', blank=True)
    background = models.ImageField(upload_to='user-backgrounds/', blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
