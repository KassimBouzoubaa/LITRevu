from django import forms
from .models import UserFollows


class FollowUserForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = []
