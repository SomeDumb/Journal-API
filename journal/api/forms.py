from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import JournalUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = JournalUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = JournalUser
        fields = ('email',)