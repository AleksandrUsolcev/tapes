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
        max_length=32,
        blank=False,
        null=False
    )
    about = models.TextField(max_length=200, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
