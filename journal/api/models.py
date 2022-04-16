from django.db import models
from django.contrib.auth.models import Group, AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class JournalUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Article(models.Model):
    topic = models.CharField(max_length=100, default='')
    text = models.TextField(default='')
    author = models.ForeignKey(JournalUser, db_column="user", on_delete=models.CASCADE)
    for_subscribers = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)