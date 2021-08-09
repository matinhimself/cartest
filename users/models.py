import datetime

from django.conf.urls import url
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()

    spouse_name = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)

    last_subscription = models.DateTimeField(default=None, blank=True, null=True)
    duration_subscription = models.DurationField(default=datetime.timedelta(days=0))

    def is_subscribed(self):
        if self.is_superuser or self.is_staff:
            return True
        if bool(
                self.last_subscription and self.duration_subscription and
                (self.last_subscription + self.duration_subscription < timezone.now())
        ):
            return True
        return False

    is_subscribed.boolean = True
