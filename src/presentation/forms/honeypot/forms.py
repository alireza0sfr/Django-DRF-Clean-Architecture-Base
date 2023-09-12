from django import forms
from domain.apps.honeypot.models import LoginAttempt


class LoginForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = LoginAttempt
        fields = ["username", "password"]
